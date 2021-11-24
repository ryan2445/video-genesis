import Vue from 'vue';
import { ValidationProvider, extend, ValidationObserver } from 'vee-validate';
import * as rules from 'vee-validate/dist/rules';

export default () => {
    Object.keys(rules).forEach(rule => {
        extend(rule, rules[rule]);
    });
    
    Vue.component('ValidationProvider', ValidationProvider);
    Vue.component('ValidationObserver', ValidationObserver);
}


// Available rules
/*
alpha
alpha_dash
alpha_num
alpha_spaces
between
confirmed
digits
dimensions
email Inferred
excluded
ext
image
oneOf
integer
is
is_not
length
max Inferred
max_value Inferred
mimes
min Inferred
min_value Inferred
numeric
regex Inferred
required Inferred
required_if
size
double
*/