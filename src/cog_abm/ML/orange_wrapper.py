"""
Module providing classifiers from orange library
"""

import orange
import core
from itertools import izip


#useful methods

def create_numeric_variable(sid, meta):
    return orange.FloatVariable(sid)

def create_nominal_variable(sid, meta):
    return orange.EnumVariable(sid, values=[str(e) for e in meta.symbols])

orange_variable_map = {
                core.NumericAttribute.ID: create_numeric_variable,
                core.NominalAttribute.ID: create_nominal_variable
                }

def create_basic_variables(meta):
    return [orange_variable_map[m.ID]("atr"+str(i), m) 
                for i,m in enumerate(meta)]


def create_domain_with_cls(meta, cls_meta):
    l = create_basic_variables(meta)
    l.append(create_nominal_variable("classAttr",cls_meta))
    return orange.Domain(l, True)
    


def _basic_convert_sample(domain, sample):
    return [orange.Value(dv, v) for dv, v in 
                    izip(domain, sample.get_values())]


def convert_sample(domain, sample):
    tmp = _basic_convert_sample(domain, sample)
    return orange.Example(domain, tmp+[None])
#this should work if cls is in domain


def convert_sample_with_cls(domain, sample):
    tmp = _basic_convert_sample(domain, sample)
    return orange.Example(domain, tmp + [domain.classVar(sample.get_cls())])
    


class OrangeClassifier(core.Classifier):
    
    
    def __init__(self, name, *args, **kargs):
        self.classifier_class = getattr(orange, name)
        self.classifier_args = args
        self.classifier_kargs = kargs
        self.classifier = self.classifier_class(*args, **kargs)
        self.domain_with_cls = None
        self.domain = None
        
    
    def classify(self, sample):
        s = convert_sample(self.domain_with_cls, sample)
        return self.classifier(s)
    
    
    # TODO: I think that parent method should be fine 
#    def clone(self):
#        return None  

    
    def train(self, samples):
        """
        Trains classifier with given samples.
        
        We recreate domain, because new class could be added
        """
        meta = samples[0].meta
        cls_meta = samples[0].cls_meta
        self.domain_with_cls = create_domain_with_cls(meta, cls_meta)
        et = orange.ExampleTable(self.domain_with_cls)
        et.extend([convert_sample_with_cls(self.domain_with_cls, s) 
                                for s in samples])
        
        self.classifier = self.classifier_class(et, *self.classifier_args, \
                                                **self.classifier_kargs)
