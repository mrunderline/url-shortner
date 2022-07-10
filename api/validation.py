# from cerberus import Validator
import validators


def validate_new_url(data):
    # schema = {
    #     'url': {
    #         'type': 'string',
    #         'maxlength': 2048,
    #         'required': True
    #     }
    # }
    # v = Validator(schema)
    # if v.validate(data):
    #     return True, data
    #
    # return False, v.errors

    if data.get('ideal_name'):
        ideal_name = data.get('ideal_name')
        if validators.length(ideal_name, min=3, max=32) is False or \
                validators.url(ideal_name) is True or \
                ' ' in ideal_name:
            return False, {'message': 'invalid ideal_name selected'}

    if validators.url(data.get('url')) is False:
        return False, {'message': 'invalid url passed'}

    return True, data
