# coding: utf-8
from __future__ import unicode_literals
from functools import wraps, partial

from yargy.compat import string_type


GENDERS = ('masc', 'femn', 'neut', 'Ms-f', 'GNdr')
NUMBERS = ('sing', 'plur', 'Sgtm', 'Pltm')
CASES = ('nomn', 'gent', 'datv', 'accs', 'ablt', 'loct', 'voct', 'Fixd')


def get_token_features(candidate, case, grammemes):
    return (
        [g in t['grammemes'] for g in grammemes] for t in (case, candidate)
    )


def type_required(type):
    def handler(func):
        @wraps(func)
        def wrapper(value, token, stack, **kwargs):
            if not isinstance(token.value, type):
                return False
            else:
                return func(value, token, stack, **kwargs)
        return wrapper
    return handler


def label(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return partial(func, *args, **kwargs)
    return wrapper


@label
def and_(labels, token, stack):
    return all(
        label(token, stack) for label in labels
    )


@label
def or_(labels, token, stack):
    return any(
        label(token, stack) for label in labels
    )


@label
@type_required(string_type)
def is_lower(value, token, stack):
    return token.value.islower() == value


@label
@type_required(string_type)
def is_upper(value, token, stack):
    return token.value.isupper() == value


@label
@type_required(string_type)
def is_title(value, token, stack):
    return token.value.istitle() == value


@label
@type_required(string_type)
def is_capitalized(value, token, stack):
    '''
    http://bugs.python.org/issue7008
    '''
    return token.value[0].isupper() == value


@label
def eq(value, token, stack):
    return token.value == value


@label
@type_required(string_type)
def length_eq(value, token, stack):
    return len(token.value) == value


@label
def not_eq(value, token, stack):
    return token.value != value


@label
@type_required(string_type)
def length_not_eq(value, token, stack):
    return len(token.value) != value


@label
def in_(value, token, stack):
    return token.value in value


@label
def not_in(value, token, stack):
    return not token.value in value


@label
@type_required((int, float))
def gt(value, token, stack):
    return token.value > value


@label
@type_required(string_type)
def length_gt(value, token, stack):
    return len(token.value) > value


@label
@type_required((int, float))
def lt(value, token, stack):
    return token.value < value


@label
@type_required(string_type)
def length_lt(value, token, stack):
    return len(token.value) < value


@label
@type_required((int, float))
def gte(value, token, stack):
    return token.value >= value


@label
@type_required(string_type)
def length_gte(value, token, stack):
    return len(token.value) >= value


@label
@type_required((int, float))
def lte(value, token, stack):
    return token.value <= value


@label
@type_required(string_type)
def length_lte(value, token, stack):
    return len(token.value) <= value


@label
def is_instance(value, token, stack):
    return isinstance(token.value, value)


@label
def custom(function, token, stack):
    return function(token, stack)


@label
def gram(value, token, stack):
    for form in token.forms:
        if value in form['grammemes']:
            return True
    return False


@label
def gram_any(values, token, stack):
    return any(gram(value)(token, stack) for value in values)


@label
def gram_in(values, token, stack):
    return all(gram(value)(token, stack) for value in values)


@label
def gram_not(value, token, stack):
    return not gram(value)(token, stack)


@label
def gram_not_in(values, token, stack):
    return all(gram_not(value)(token, stack) for value in values)


def match_labels_with_disabmiguation_resolving(index, token, stack, match_labels, solve_disambiguation=False, match_all_disambiguation_forms=True):

    if solve_disambiguation:
        case_forms = []
        candidate_forms = []

    for candidate_form in token.forms:
        if not match_all_disambiguation_forms:
            if case_forms and candidate_forms:
                break
        for case_form in stack[index].forms:
            match = all(
                label(candidate_form, case_form) for label in match_labels
            )
            if match:
                if solve_disambiguation:
                    if not case_form in case_forms:
                        case_forms.append(case_form)
                    if not candidate_form in candidate_forms:
                        candidate_forms.append(candidate_form)
                    if not match_all_disambiguation_forms:
                        break
                else:
                    return True

    if solve_disambiguation and (case_forms and candidate_forms):
        if case_forms and candidate_forms:
            token.forms = candidate_forms
            stack[index].forms = case_forms
            return True

    return False


def gender_match_check(candidate, case, genders=GENDERS):
    results = get_token_features(candidate, case, genders)

    case_token_results = next(results)
    case_token_msf, case_token_gndr = (
        case_token_results[-2],
        case_token_results[-1],
    )
    case_token_genders = case_token_results[:-2]

    candidate_token_results = next(results)
    candidate_token_msf, candidate_token_gndr = (
        candidate_token_results[-2],
        candidate_token_results[-1],
    )
    candidate_token_genders = candidate_token_results[:-2]

    if not candidate_token_genders == case_token_genders:
        if case_token_msf:
            if any(candidate_token_genders[:2]):
                return True
        if candidate_token_msf:
            if any(case_token_genders[:2]):
                return True
        elif case_token_gndr or candidate_token_gndr:
            return True
        elif 'plur' in case['grammemes'] and 'plur' in candidate['grammemes']:
            return True
        else:
            if (case_token_genders[0] and candidate_token_genders[0]) or \
               (case_token_genders[1] and candidate_token_genders[1]) or \
               (case_token_genders[2] and candidate_token_genders[2]):
                return True
    else:
        return True


@label
@type_required(string_type)
def gender_match(*args, **kwargs):
    return match_labels_with_disabmiguation_resolving(*args, match_labels=[
        gender_match_check,
    ], **kwargs)


def number_match_check(candidate, case, numbers=NUMBERS):
    results = get_token_features(candidate, case, numbers)

    case_form_results = next(results)
    case_form_features, case_form_only_sing, case_form_only_plur = (
        case_form_results[:-2],
        case_form_results[-2],
        case_form_results[-1],
    )

    candidate_form_results = next(results)
    candidate_form_features, candidate_form_only_sing, candidate_form_only_plur = (
        candidate_form_results[:-2],
        candidate_form_results[-2],
        candidate_form_results[-1],
    )

    if case_form_features == candidate_form_features:
        return True
    elif case_form_only_sing or case_form_only_plur:
        if case_form_only_sing:
            if candidate_form_features[0]:
                return True
        elif case_form_only_plur:
            if candidate_form_features[1]:
                return True


@label
@type_required(string_type)
def number_match(*args, **kwargs):
    return match_labels_with_disabmiguation_resolving(*args, match_labels=[
        number_match_check,
    ], **kwargs)


def case_match_check(candidate, case, cases=CASES):
    results = get_token_features(candidate, case, cases)

    case_form_results = next(results)
    case_form_features, is_case_fixed = (
        case_form_results[:-1],
        case_form_results[-1],
    )

    candidate_form_results = next(results)
    candidate_form_features, is_candidate_fixed = (
        candidate_form_results[:-1],
        candidate_form_results[-1],
    )

    if case_form_features == candidate_form_features:
        return True
    elif is_case_fixed or is_candidate_fixed:
        return True


@label
@type_required(string_type)
def case_match(*args, **kwargs):
    return match_labels_with_disabmiguation_resolving(*args, match_labels=[
        case_match_check,
    ], **kwargs)


@label
@type_required(string_type)
def gnc_match(*args, **kwargs):
    return match_labels_with_disabmiguation_resolving(*args, match_labels=[
        gender_match_check,
        number_match_check,
        case_match_check
    ], **kwargs)


@label
@type_required(string_type)
def dictionary(values, token, stack):
    return any((form['normal_form'] in values) for form in token.forms)


@label
@type_required(string_type)
def dictionary_not(values, token, stack):
    return not dictionary(values)(token, stack)


def get_token_prediction_methods(token):
    for form in token.forms: # iterate over all word forms returned by pymorphy2
        methods = form.get('methods_stack', None) # https://github.com/kmike/pymorphy2/issues/89#issuecomment-278016091
        if methods: # methods_stack attribute avaible only for russian words
            for method in methods:
                yield method[0] # return only method name, e.g. DictionaryAnalyzer / KnownSuffixAnalyzer


@label
@type_required(string_type)
def is_predicted(value, token, stack):
    prediction_methods = set(
        get_token_prediction_methods(token)
    )

    # Uncomment this lines to see more info about pymorphy2 word lookup methods
    # print('Token value:', token.value)
    # print('Token lookup methods:', prediction_methods)

    prediction_methods_names = set(
        # use class names, because pymorphy2 units isn't global singleton objects,
        # e.g. DictionaryAnalyzer() and DictionaryAnalyzer() are different objects
        m.__class__.__name__ for m in prediction_methods
    )

    is_predicted_word = not (
        'DictionaryAnalyzer' in prediction_methods_names
    )

    return value == is_predicted_word
