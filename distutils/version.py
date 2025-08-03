import re

class LooseVersion:
    _component_re = re.compile(r"(\d+|[a-z]+|\.)", re.I)

    def __init__(self, version=""):
        self.version = version
        self.version = self.parse(self.version)

    def parse(self, vstring):
        parts = []
        for part in self._component_re.findall(vstring):
            if part.isdigit():
                parts.append(int(part))
            else:
                parts.append(part.lower())
        return parts

    def __repr__(self):
        return f"<LooseVersion: {self}>"

    def __str__(self):
        return "".join(str(p) for p in self.version)

    def _cmp(self, other):
        if not isinstance(other, LooseVersion):
            other = LooseVersion(other)
        v1 = self.version
        v2 = other.version
        length = max(len(v1), len(v2))
        for i in range(length):
            a = v1[i] if i < len(v1) else 0
            b = v2[i] if i < len(v2) else 0
            if a != b:
                return (a > b) - (a < b)
        return 0

    def __lt__(self, other):
        return self._cmp(other) < 0

    def __le__(self, other):
        return self._cmp(other) <= 0

    def __eq__(self, other):
        return self._cmp(other) == 0

    def __ne__(self, other):
        return self._cmp(other) != 0

    def __gt__(self, other):
        return self._cmp(other) > 0

    def __ge__(self, other):
        return self._cmp(other) >= 0
