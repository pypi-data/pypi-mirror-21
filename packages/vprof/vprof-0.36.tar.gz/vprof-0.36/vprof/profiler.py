"""Module for Python profiler wrapper."""
import cProfile
import operator
import pstats
import runpy

from vprof import base_profiler


class Profiler(base_profiler.BaseProfiler):
    """Python profiler wrapper.

    Runs cProfile against specified program and returns obtained stats.
    """

    def _transform_stats(self, prof):
        """Post-processes obtained stats for UI."""
        records = []
        for info, params in prof.stats.items():
            filename, lineno, funcname = info
            cum_calls, num_calls, time_per_call, cum_time, _ = params
            if prof.total_tt == 0:
                percentage = 0
            else:
                percentage = round(100 * (cum_time / prof.total_tt), 4)
            cum_time = round(cum_time, 4)
            funcname = funcname.replace('<', '[').replace('>', ']')
            filename = filename.replace('<', '[').replace('>', ']')
            func_name = '%s @ %s' % (funcname, filename)
            color_hash = base_profiler.hash_name(func_name)
            records.append(
                (filename, lineno, funcname, cum_time, percentage, num_calls,
                 cum_calls, time_per_call, filename, color_hash))
        return sorted(records, key=operator.itemgetter(4), reverse=True)

    @base_profiler.run_in_another_process
    def profile_package(self):
        """Runs cProfile on package."""
        prof = cProfile.Profile()
        prof.enable()
        try:
            runpy.run_path(self._run_object, run_name='__main__')
        except SystemExit:
            pass
        prof.disable()
        prof_stats = pstats.Stats(prof)
        prof_stats.calc_callees()
        return {
            'objectName': self._object_name,
            'callStats': self._transform_stats(prof_stats),
            'totalTime': prof_stats.total_tt,
            'primitiveCalls': prof_stats.prim_calls,
            'totalCalls': prof_stats.total_calls,
        }

    @base_profiler.run_in_another_process
    def profile_module(self):
        """Runs cProfile on module."""
        prof = cProfile.Profile()
        try:
            with open(self._run_object, 'rb') as srcfile:
                code = compile(srcfile.read(), self._run_object, 'exec')
            prof.runctx(code, self._globs, None)
        except SystemExit:
            pass
        prof_stats = pstats.Stats(prof)
        prof_stats.calc_callees()
        return {
            'objectName': self._object_name,
            'callStats': self._transform_stats(prof_stats),
            'totalTime': prof_stats.total_tt,
            'primitiveCalls': prof_stats.prim_calls,
            'totalCalls': prof_stats.total_calls,
        }

    def profile_function(self):
        """Runs cProfile on function."""
        prof = cProfile.Profile()
        prof.enable()
        self._run_object(*self._run_args, **self._run_kwargs)
        prof.disable()
        prof_stats = pstats.Stats(prof)
        prof_stats.calc_callees()
        return {
            'objectName': self._object_name,
            'callStats': self._transform_stats(prof_stats),
            'totalTime': prof_stats.total_tt,
            'primitiveCalls': prof_stats.prim_calls,
            'totalCalls': prof_stats.total_calls,
        }
