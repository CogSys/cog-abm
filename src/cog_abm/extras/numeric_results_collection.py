import json

from itertools import izip

from cog_abm.extras.tools import ext


class NumericResultCollector(object):

    ERR_SUFIX = '||ERR'
    ''' This is suffix of the name that is given to stdev of given column
    '''

    def __init__(self, columns=None, column_names=None):
        self.columns = columns or []
        self.column_names = column_names or []

    def add_column(self, column_values, column_name=''):
        if column_name:
            self.column_names.append((len(self.columns), column_name))
        self.columns.append(column_values)

    def add_column_with_err(self, column_values, column_name='', err_column_name=''):
        err_col_name = err_column_name or (column_name + self.ERR_SUFIX)
        for col, col_name in ((ext(column_values, 0), column_name),
                              (ext(column_values, 1), err_col_name)):
            self.add_column(col, col_name)

    def iter_results_table(self):
        return izip(*self.columns)

    def iter_by_columns(self):
        for i, c in enumerate(self.columns):
            yield self.column_names[i][1], c

    def iter_by_columns_with_errs(self):
        for i in xrange(0, len(self.columns), 2):
            yield self.column_names[i][1], \
                zip(self.columns[i], self.columns[i + 1])

    def iter_smart_columns(self):
        i = 0
        while i < len(self.columns):
            i1 = i + 1
            name = self.column_names[i][1]
            if i1 < len(self.columns) and \
                    name + self.ERR_SUFIX == self.column_names[i1][1]:
                yield name, zip(self.columns[i], self.columns[i + 1])
                i += 2
            else:
                yield name, (self.columns[i], self.columns[i])
                i += 1

    def _save(self, f):
        f.write('# {0}\n'.format(json.dumps(self.column_names)))
        for r in self.iter_results_table():
            f.write('{0}\n'.format('\t'.join((str(x) for x in r))))

    def save(self, fname):
        with open(fname, 'w') as f:
            self._save(f)

    @classmethod
    def load(cls, fname):
        with open(fname, 'r') as f:
            return cls._load(f)

    @classmethod
    def _load(cls, f):
        lines = f.readlines()
        comment = lines[0].strip('# \n')
        column_names = [tuple(l) for l in json.loads(comment)]
        columns = [[float(f) for f in l.split('\t')]
                        for l in lines[1:] if l.strip()]
        columns = zip(*columns)
        return cls(columns, column_names)

