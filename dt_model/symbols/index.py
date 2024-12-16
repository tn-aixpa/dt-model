from __future__ import annotations

from typing import Any

from sympy import lambdify
from scipy import stats

from dt_model.symbols._base import SymbolExtender
from dt_model.symbols.context_variable import ContextVariable


class Index(SymbolExtender):
    """
    Class to represent an index variable.
    """

    def __init__(self, name: str, value: Any, cvs: list[ContextVariable] | None = None, group: str | None = None) -> None:
        super().__init__(name)
        self.group = group
        self.cvs = cvs
        if cvs is not None:
            self.value = lambdify(cvs, value, "numpy")
        else:
            self.value = value

class UniformDistIndex(Index):
    """
    Class to represent an index as a uniform distribution
    """

    def __init__(self, name: str, loc: float, scale: float, group: str | None = None) -> None:
        super().__init__(name, stats.uniform(loc=loc, scale=scale), group=group)
        self._loc = loc
        self._scale = scale

    @property
    def loc(self):
        return self._loc

    @loc.setter
    def loc(self, new_loc):
        if self._loc != new_loc:
            self._loc = new_loc
            self.value = stats.uniform(loc=self._loc, scale=self._scale)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, new_scale):
        if self._scale != new_scale:
            self._scale = new_scale
            self.value = stats.uniform(loc=self._loc, scale=self._scale)

    def __str__(self):
        return f"uniform_dist_idx({self.loc}, {self.scale})"

class LognormDistIndex(Index):
    """
    Class to represent an index as a longnorm distribution
    """

    def __init__(self, name: str, loc: float, scale: float, s: float, group: str | None = None) -> None:
        super().__init__(name, stats.lognorm(loc=loc, scale=scale, s=s), group=group)
        self._loc = loc
        self._scale = scale
        self._s = s

    @property
    def loc(self):
        return self._loc

    @loc.setter
    def loc(self, new_loc):
        if self._loc != new_loc:
            self._loc = new_loc
            self.value = stats.lognorm(loc=self._loc, scale=self._scale, s=self.s)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, new_scale):
        if self._scale != new_scale:
            self._scale = new_scale
            self.value = stats.lognorm(loc=self._loc, scale=self._scale, s=self._s)

    @property
    def s(self):
        return self._s

    @s.setter
    def s(self, new_s):
        if self._s != new_s:
            self._s = new_s
            self.value = stats.lognorm(loc=self._loc, scale=self._scale, s=self._s)

    def __str__(self):
        return f"longnorm_dist_idx({self.loc}, {self.scale}, {self.s})"


class TriangDistIndex(Index):
    """
    Class to represent an index as a longnorm distribution
    """

    def __init__(self, name: str, loc: float, scale: float, c: float, group: str | None = None) -> None:
        super().__init__(name, stats.triang(loc=loc, scale=scale, c=c), group=group)
        self._loc = loc
        self._scale = scale
        self._c = c

    @property
    def loc(self):
        return self._loc

    @loc.setter
    def loc(self, new_loc):
        if self._loc != new_loc:
            self._loc = new_loc
            self.value = stats.triang(loc=self._loc, scale=self._scale, c=self._c)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, new_scale):
        if self._scale != new_scale:
            self._scale = new_scale
            self.value = stats.triang(loc=self._loc, scale=self._scale, c=self._c)

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, new_c):
        if self._c != new_c:
            self._c = new_c
            self.value = stats.triang(loc=self._loc, scale=self._scale, c=self._c)

    def __str__(self):
        return f"triang_dist_idx({self.loc}, {self.scale}, {self.c})"

class ConstIndex(Index):
    """
    Class to represent an index as a longnorm distribution
    """

    def __init__(self, name: str, v: float, group: str | None = None) -> None:
        super().__init__(name, v, group=group)
        self._v = v

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, new_v):
        if self._v != new_v:
            self._v = new_v
            self.value = new_v

    def __str__(self):
        return f"const_idx({self.v})"

class SymIndex(Index):
    """
    Class to represent an index as a symbolic value
    """

    def __init__(self,
                 name: str,
                 value: Any,
                 cvs: list[ContextVariable] | None = None,
                 group: str | None = None
                ) -> None:
        super().__init__(name, value, cvs, group=group)
        self._cvs = cvs
        if cvs is not None:
            self._value = lambdify(cvs, value, "numpy")
        else:
            self._value = value

        self._sym_value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value != new_value:
            if self._cvs is not None:
                self._value = lambdify(self._cvs, new_value, "numpy")
            else:
                self._value = new_value
            self._sym_value = new_value

    @property
    def sym_value(self):
        return self._sym_value

    @sym_value.setter
    def sym_value(self, new_value):
        if self._sym_value != new_value:
            if self._cvs is not None:
                self._value = lambdify(self._cvs, new_value, "numpy")
            else:
                self._value = new_value
            self._sym_value = new_value

    @property
    def cvs(self):
        return self._cvs

    @cvs.setter
    def cvs(self, new_cvs):
        if self._cvs != new_cvs:
            self._cvs = new_cvs
            if self._cvs is not None:
                self._value = lambdify(self._cvs, self._sym_value, "numpy")

    def __str__(self):
        return f"sympy_idx({self.value})"

