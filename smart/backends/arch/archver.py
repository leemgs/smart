#
# Copyright (c) 2004 Conectiva, Inc.
#
# Written by Gustavo Niemeyer <niemeyer@conectiva.com>
#
# Archlinux module written by Cody Lee (aka. platinummonkey) <platinummonkey@archlinux.us>
#
# This file is part of Smart Package Manager.
#
# Smart Package Manager is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# Smart Package Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Smart Package Manager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
from smart import *
import re

VERRE = re.compile("([^-]+)(?:-([^-]+)(?:-(.+))?)?")

def splitarch(v):
    slash = v.rfind("-")
    if slash == -1:
        return v, None
    toks = v.rsplit("-")
    return toks[-1]

def splitrelease(v):
    slash = v.rfind("-")
    if slash == -1:
        return v, None
    toks = v.rsplit("-")
    return toks[-2]

def checkdep(s1, rel, s2):
    cmp = vercmp(s1, s2)
    if cmp == 0:
        return '=' in rel
    elif cmp < 0:
        return '<' in rel
    else:
        return '>' in rel

def vercmp(s1, s2):
    return vercmpparts(*(VERRE.match(s1).groups()+VERRE.match(s2).groups()))

# compare alpha and numeric segments of two versions
# return 1: first is newer than second
#        0: first and second are the same version
#       -1: second is newer than first
def vercmpparts(v1, a1, b1, v2, a2, b2):
    rc = vercmppart(v1, v2)
    if rc:
        return rc
    elif not b1 or not b2:
        return 0
    i1 = 0
    i2 = 0
    lb1 = len(b1)
    lb2 = len(b2)
    while i1 < lb1 and b1[i1].isdigit(): i1 += 1
    while i2 < lb2 and b2[i2].isdigit(): i2 += 1
    return vercmppart(b1[:i1], b2[:i2])

# compare alpha and numeric segments of two versions
# return 1: a is newer than b
#        0: a and b are the same version
#       -1: b is newer than a
def vercmppart(a, b):
    if a == b:
        return 0
    ai = 0
    bi = 0
    la = len(a)
    lb = len(b)
    while ai < la and bi < lb:
        while ai < la and not a[ai].isalnum(): ai += 1
        while bi < lb and not b[bi].isalnum(): bi += 1
        aj = ai
        bj = bi
        if a[aj].isdigit():
            while aj < la and a[aj].isdigit(): aj += 1
            while bj < lb and b[bj].isdigit(): bj += 1
            isnum = 1
        else:
            while aj < la and a[aj].isalpha(): aj += 1
            while bj < lb and b[bj].isalpha(): bj += 1
            isnum = 0
        if aj == ai:
            return -1
        if bj == bi:
            return isnum and 1 or -1
        if isnum:
            while ai < la and a[ai] == '0': ai += 1
            while bi < lb and b[bi] == '0': bi += 1
            if aj-ai > bj-bi: return 1
            if bj-bi > aj-ai: return -1
        rc = cmp(a[ai:aj], b[bi:bj])
        if rc:
            return rc
        ai = aj
        bi = bj
    if ai == la and bi == lb:
        return 0
    if ai == la:
        return -1
    else:
        return 1

def enablePsyco(psyco):
    psyco.bind(vercmppart)
    psyco.bind(vercmpparts)

hooks.register("enable-psyco", enablePsyco)

# vim:ts=4:sw=4
