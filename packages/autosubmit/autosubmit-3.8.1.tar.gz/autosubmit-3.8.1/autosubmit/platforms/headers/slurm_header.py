#!/usr/bin/env python

# Copyright 2017 Earth Sciences Department, BSC-CNS

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

import textwrap


class SlurmHeader(object):
    """Class to handle the SLURM headers of a job"""

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def get_queue_directive(self, job):
        """
        Returns queue directive for the specified job

        :param job: job to create queue directive for
        :type job: Job
        :return: queue directive
        :rtype: str
        """
        # There is no queue, so directive is empty
        if job.parameters['CURRENT_QUEUE'] == '':
            return ""
        else:
            return "SBATCH -p {0}".format(job.parameters['CURRENT_QUEUE'])

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def get_account_directive(self, job):
        """
        Returns account directive for the specified job

        :param job: job to create account directive for
        :type job: Job
        :return: account directive
        :rtype: str
        """
        # There is no account, so directive is empty
        if job.parameters['CURRENT_PROJ'] != '':
            return "SBATCH -A {0}".format(job.parameters['CURRENT_PROJ'])
        return ""

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def get_memory_directive(self, job):
        """
        Returns memory directive for the specified job

        :param job: job to create memory directive for
        :type job: Job
        :return: memory directive
        :rtype: str
        """
        # There is no memory, so directive is empty
        if job.parameters['MEMORY'] != '':
            return "SBATCH --mem {0}".format(job.parameters['MEMORY'])
        return ""

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def get_memory_per_task_directive(self, job):
        """
        Returns memory per task directive for the specified job

        :param job: job to create memory per task directive for
        :type job: Job
        :return: memory per task directive
        :rtype: str
        """
        # There is no memory per task, so directive is empty
        if job.parameters['MEMORY_PER_TASK'] != '':
            return "SBATCH --mem-per-cpu {0}".format(job.parameters['MEMORY_PER_TASK'])
        return ""

    SERIAL = textwrap.dedent("""\
            ###############################################################################
            #                   %TASKTYPE% %EXPID% EXPERIMENT
            ###############################################################################
            #
            #%QUEUE_DIRECTIVE%
            #%ACCOUNT_DIRECTIVE%
            #%MEMORY_DIRECTIVE%
            #%MEMORY_PER_TASK_DIRECTIVE%
            #SBATCH -n %NUMPROC%
            #SBATCH -t %WALLCLOCK%:00
            #SBATCH -J %JOBNAME%
            #SBATCH -o %CURRENT_SCRATCH_DIR%/%CURRENT_PROJ%/%CURRENT_USER%/%EXPID%/LOG_%EXPID%/%OUT_LOG_DIRECTIVE%
            #SBATCH -e %CURRENT_SCRATCH_DIR%/%CURRENT_PROJ%/%CURRENT_USER%/%EXPID%/LOG_%EXPID%/%ERR_LOG_DIRECTIVE%
            #
            ###############################################################################
           """)

    PARALLEL = textwrap.dedent("""\
            ###############################################################################
            #                   %TASKTYPE% %EXPID% EXPERIMENT
            ###############################################################################
            #
            #%QUEUE_DIRECTIVE%
            #%ACCOUNT_DIRECTIVE%
            #%MEMORY_DIRECTIVE%
            #%MEMORY_PER_TASK_DIRECTIVE%
            #SBATCH -n %NUMPROC%
            #SBATCH -t %WALLCLOCK%:00
            #SBATCH -J %JOBNAME%
            #SBATCH -o %CURRENT_SCRATCH_DIR%/%CURRENT_PROJ%/%CURRENT_USER%/%EXPID%/LOG_%EXPID%/%OUT_LOG_DIRECTIVE%
            #SBATCH -e %CURRENT_SCRATCH_DIR%/%CURRENT_PROJ%/%CURRENT_USER%/%EXPID%/LOG_%EXPID%/%ERR_LOG_DIRECTIVE%
            #
            ###############################################################################
            """)
