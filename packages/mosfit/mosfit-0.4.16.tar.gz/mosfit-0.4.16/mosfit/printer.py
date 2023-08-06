# -*- coding: utf-8 -*-
"""Defines the `Printer` class."""
from __future__ import print_function

import datetime
import json
import os
import sys
from builtins import input
from textwrap import fill

import numpy as np

from .utils import calculate_WAIC, is_integer, pretty_num

if sys.version_info[:2] < (3, 3):
    old_print = print  # noqa

    def print(*args, **kwargs):
        """Replacement for print function in Python 2.x."""
        flush = kwargs.pop('flush', False)
        old_print(*args, **kwargs)
        file = kwargs.get('file', sys.stdout)
        if flush and file is not None:
            file.flush()


class Printer(object):
    """Print class for MOSFiT."""

    class bcolors(object):
        """Special formatting characters."""

        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        CYAN = '\033[96m'
        MAGENTA = '\033[1;35m'
        ORANGE = '\033[38;5;214m'

        codes = {
            '!e': ENDC,
            '!m': MAGENTA,
            '!y': WARNING,
            '!b': OKBLUE,
            '!r': FAIL,
            '!g': OKGREEN,
            '!u': UNDERLINE,
            '!c': CYAN
        }

    def __init__(self, pool=None, wrap_length=100, quiet=False, fitter=None,
                 language='en'):
        """Initialize printer, setting wrap length."""
        self._wrap_length = wrap_length
        self._quiet = quiet
        self._pool = pool
        self._fitter = fitter
        self._language = language

        self.set_strings()

    def set_strings(self):
        """Set pre-defined list of strings."""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path, 'strings.json')) as f:
            strings = json.load(f)
        if self._language == 'en':
            self._strings = strings
            return
        lsf = os.path.join(dir_path, 'strings-' + self._language + '.json')
        if os.path.isfile(lsf):
            with open(lsf) as f:
                self._strings = json.load(f)
            if set(self._strings.keys()) == set(strings):
                return

        try:
            from googletrans import Translator  # noqa
        except Exception:
            self.wrapped(
                'The `--language` option requires the `Googletrans` package. '
                'Please install with `pip install googletrans`.')
            self._strings = strings
            pass
        else:
            self.wrapped(self.translate(
                'Building strings for `{}`, please wait...'
                .format(self._language)))
            self._strings = {}
            for key in strings:
                self._strings[key] = self.translate(strings[key])
            with open(lsf, 'w') as f:
                json.dump(self._strings, f)

    def set_language(self, language):
        """Set language."""
        self._language = language

    def colorify(self, text):
        """Add colors to text."""
        output = text
        for code in self.bcolors.codes:
            output = output.replace(code, self.bcolors.codes[code])
        return output

    def prt(self, text):
        """Print text without modification."""
        if self._quiet:
            return
        print(text)

    def message(self, name, reps=[], wrapped=True, inline=False,
                warning=False, error=False, prefix=True):
        """Print a message from a dictionary of strings."""
        if name in self._strings:
            text = self._strings[name]
        else:
            text = '< Message not found [' + ''.join(
                ['{} ' for x in range(len(reps))]).strip() + '] >'
        text = text.format(*reps)
        if wrapped:
            self.wrapped(text, warning=warning, error=error, prefix=prefix)
        elif inline:
            self.inline(text, warning=warning, error=error, prefix=prefix)
        else:
            self.prt(text)

    def inline(self, x, new_line=False,
               warning=False, error=False, prefix=True):
        """Print inline, erasing underlying pre-existing text."""
        if self._quiet:
            return
        lines = x.split('\n')
        if warning:
            sys.stdout.write(self.bcolors.WARNING)
            if prefix and len(lines):
                lines[0] = self._strings['warning'] + ': ' + lines[0]
        if error:
            sys.stdout.write(self.bcolors.FAIL)
            if prefix and len(lines):
                lines[0] = self._strings['error'] + ': ' + lines[0]
        if not new_line:
            for line in lines:
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
        print(x, flush=True)
        if error or warning:
            sys.stdout.write(self.bcolors.ENDC)

    def wrapped(self, text, wrap_length=None, master_only=True, warning=False,
                error=False, prefix=True):
        """Print text wrapped to either the specified length or the default."""
        if self._quiet:
            return
        if wrap_length and is_integer(wrap_length):
            wl = wrap_length
        else:
            wl = self._wrap_length
        if master_only and self._pool and not self._pool.is_master():
            return
        if warning:
            sys.stdout.write(self.bcolors.WARNING)
            if prefix:
                text = self._strings['warning'] + ': ' + text
        if error:
            sys.stdout.write(self.bcolors.FAIL)
            if prefix:
                text = self._strings['error'] + ': ' + text
        print(fill(text, wl))
        if error or warning:
            sys.stdout.write(self.bcolors.ENDC)

    def prompt(self, text, wrap_length=None, kind='bool',
               none_string='None of the above.',
               options=None, translate=True):
        """Prompt the user for input and return a value based on response."""
        if wrap_length and is_integer(wrap_length):
            wl = wrap_length
        else:
            wl = self._wrap_length

        if kind == 'bool':
            choices = ' (y/[n])'
        elif kind == 'select':
            selpad = ''.join([' ' for x in str(len(options))])
            choices = '\n' + '\n'.join([
                ' ' + str(i + 1) + '. ' + selpad[len(str(i + 1)) - 1:] +
                options[i] for i in range(len(options))
            ] + [
                '[n].' + selpad + none_string + '\n' +
                'Enter selection (' + ('1-' if len(options) > 1 else '') + str(
                    len(options)) + '/[n]):'
            ])
        elif kind == 'string':
            choices = ''
        else:
            raise ValueError('Unknown prompt kind.')

        textchoices = text + choices
        if translate:
            textchoices = self.translate(textchoices)
        prompt_txt = (textchoices).split('\n')
        for txt in prompt_txt[:-1]:
            ptxt = fill(txt, wl, replace_whitespace=False)
            print(ptxt)
        user_input = input(
            fill(
                prompt_txt[-1], wl, replace_whitespace=False) + " ")
        if kind == 'bool':
            return user_input in ["Y", "y", "Yes", "yes"]
        elif kind == 'select':
            if (is_integer(user_input) and
                    int(user_input) in list(range(1, len(options) + 1))):
                return options[int(user_input) - 1]
            return False
        elif kind == 'string':
            return user_input

    def status(self,
               fitter,
               desc='',
               scores='',
               accepts='',
               progress='',
               acor=None,
               psrf=None,
               fracking=False,
               messages=[]):
        """Print status message showing state of fitting process."""
        if self._quiet:
            return

        outarr = [fitter._event_name]
        if desc:
            if desc == 'burning':
                descstr = self.bcolors.ORANGE + self._strings.get(
                    desc, '?') + self.bcolors.ENDC
            else:
                descstr = self._strings.get(desc, '?')
            outarr.append(descstr)
        if isinstance(scores, list):
            scorestring = self._strings[
                'fracking_scores'] if fracking else self._strings[
                    'score_ranges']
            scorestring += ': [ ' + ', '.join([
                '...'.join([
                    pretty_num(min(x))
                    if not np.isnan(min(x)) and np.isfinite(min(x))
                    else 'NaN',
                    pretty_num(max(x))
                    if not np.isnan(max(x)) and np.isfinite(max(x))
                    else 'NaN']) if len(x) > 1 else pretty_num(x[0])
                for x in scores
            ]) + ' ]'
            outarr.append(scorestring)
            if not fracking:
                scorestring = 'WAIC: ' + pretty_num(calculate_WAIC(scores))
                outarr.append(scorestring)
        if isinstance(accepts, list):
            scorestring = self._strings['moves_accepted'] + ': [ '
            scorestring += ', '.join([
                (self.bcolors.FAIL if x < 0.01 else
                 (self.bcolors.WARNING if x < 0.1 else
                  self.bcolors.OKGREEN)) +
                '{:.0%}'.format(x) + self.bcolors.ENDC
                for x in accepts
            ]) + ' ]'
            outarr.append(scorestring)
        if isinstance(progress, list):
            if progress[1]:
                progressstring = (
                    self._strings['progress'] +
                    ': [ {}/{} ]'.format(*progress))
            else:
                progressstring = (
                    self._strings['progress'] + ': [ {} ]'.format(progress[0]))
            outarr.append(progressstring)
        if fitter._emcee_est_t < 0.0:
            outarr.append(self._strings['run_until_converged'])
        elif fitter._emcee_est_t + fitter._bh_est_t > 0.0:
            if fitter._bh_est_t > 0.0 or not fitter._fracking:
                tott = fitter._emcee_est_t + fitter._bh_est_t
            else:
                tott = 2.0 * fitter._emcee_est_t
            timestring = self.get_timestring(tott)
            outarr.append(timestring)
        if acor is not None:
            acorcstr = pretty_num(acor[1], sig=3)
            if acor[0] <= 0.0:
                acorstring = (self.bcolors.FAIL +
                              'Chain too short for `acor` ({})'.format(
                                  acorcstr) + self.bcolors.ENDC)
            else:
                acortstr = pretty_num(acor[0], sig=3)
                acorbstr = str(int(acor[2]))
                if acor[1] < 2.0:
                    col = self.bcolors.FAIL
                elif acor[1] < 5.0:
                    col = self.bcolors.WARNING
                else:
                    col = self.bcolors.OKGREEN
                acorstring = col
                acorstring = acorstring + 'Acor Tau (i > {}): {} ({}x)'.format(
                    acorbstr, acortstr, acorcstr)
                acorstring = acorstring + (self.bcolors.ENDC if col else '')
            outarr.append(acorstring)
        if psrf is not None and psrf[0] != np.inf:
            psrfstr = pretty_num(psrf[0], sig=4)
            psrfbstr = str(int(psrf[1]))
            if psrf[0] > 2.0:
                col = self.bcolors.FAIL
            elif psrf[0] > 1.2:
                col = self.bcolors.WARNING
            else:
                col = self.bcolors.OKGREEN
            psrfstring = col
            psrfstring = psrfstring + 'PSRF (i > {}): {}'.format(
                psrfbstr, psrfstr)
            psrfstring = psrfstring + (self.bcolors.ENDC if col else '')
            outarr.append(psrfstring)

        if not isinstance(messages, list):
            raise ValueError('`messages` must be list!')
        outarr.extend(messages)

        line = ''
        lines = ''
        li = 0
        for i, item in enumerate(outarr):
            oldline = line
            line = line + (' | ' if li > 0 else '') + item
            li = li + 1
            if len(line) > self._wrap_length:
                li = 1
                lines = lines + '\n' + oldline
                line = item

        lines = lines + '\n' + line

        self.inline(lines, new_line=fitter._test)

    def get_timestring(self, t):
        """Return estimated time remaining.

        Return a string showing the estimated remaining time based upon
        elapsed times for emcee and fracking.
        """
        td = str(datetime.timedelta(seconds=int(round(t))))
        return (self._strings['estimated_time'] + ': [ ' + td + ' ]')

    def translate(self, text):
        """Translate text to another language."""
        if self._language != 'en':
            try:
                from googletrans import Translator
                translator = Translator()
                text = translator.translate(text, dest=self._language).text
            except Exception:
                pass
        return text

    def tree(self, my_tree):
        """Pretty print the module dependency trees for each root."""
        for root in my_tree:
            tree_str = json.dumps({root: my_tree[root]},
                                  indent='─ ',
                                  separators=('', ''))
            tree_str = ''.join(
                c for c in tree_str if c not in ['{', '}', '"'])
            tree_str = '\n'.join([
                x.rstrip() for x in tree_str.split('\n') if
                x.strip('─ ') != ''])
            tree_str = '\n'.join(
                [x[::-1].replace('─ ─', '├', 1)[::-1].replace('─', '│') if
                 x.startswith('─ ─') else x.replace('─ ', '') + ':'
                 for x in tree_str.split('\n')])
            lines = ['  ' + x for x in tree_str.split('\n')]
            ll = len(lines)
            for li, line in enumerate(lines):
                if (li < ll - 1 and
                        lines[li + 1].count('│') < line.count('│')):
                    lines[li] = line.replace('├', '└')
            for li, line in enumerate(reversed(lines)):
                if li == 0:
                    lines[ll - li - 1] = line.replace(
                        '│', ' ').replace('├', '└')
                    continue
                lines[ll - li - 1] = ''.join([
                    x if ci > len(lines[ll - li]) - 1 or x not in ['│', '├'] or
                    lines[ll - li][ci] != ' ' else x.replace(
                        '│', ' ').replace(
                            '├', '└') for ci, x in enumerate(line)])
            tree_str = '\n'.join(lines)
            print(tree_str)
