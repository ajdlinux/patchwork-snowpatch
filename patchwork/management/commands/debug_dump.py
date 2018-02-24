# Patchwork - automated patch tracking system
# Copyright (C) 2018 Daniel Axtens <dja@axtens.net>
#
# This file is part of the Patchwork package.
#
# Patchwork is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Patchwork is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from django.core.management import base

from patchwork.models import Patch
from patchwork.models import Series


class Command(base.BaseCommand):
    help = 'DEBUG COMMAND: Return a minimal robust representation of the db.'

    def handle(self, *args, **options):
        """This is to check the invariance of parsing as messages are
        reordered or received in parallel."""

        series = []
        for s in Series.objects.all():
            series += ['%s :: v%d :: %d patches :: %s'
                       % (s.name, s.version, s.total, s.submitter.email)]

        series.sort()
        print('=== %d series ===' % len(series))
        for s in series:
            print(s)

        patches = []
        for p in Patch.objects.all():
            patches += ['%s :: ID %s' % (p.name, p.msgid)]

        patches.sort()
        print('=== %d patches ===' % len(patches))
        for p in patches:
            print(p)
