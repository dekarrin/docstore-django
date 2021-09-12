from django.core.serializers import serialize, deserialize

import json


class ModelParseError(Exception):
    """
    Raised by deserialize_models if there is an issue with the format of the
    encoded models being parsed.
    """
    pass


def serialize_models(model_or_models, **options):
    """
    Serialize a django Model or an iterable of Models to a JSON string. If a
    single non-iterable Model is passed in, a string containing that Model's
    JSON representation is returned; otherwise, a string containing a JSON list
    with all the provided Models's JSON represntations is returned.

    If keyword args are specified, they are passed to django.core.serializers's
    serialize function as its 'options' kwargs parameters.
    """

    # TODO: ensure GET URI is included in output

    try:
        json_data = serialize('json', model_or_models, **options)

        # Django does special treatment of the Model serialization to preserve
        # it over the network, so we need to adjust the output to look more as
        # a consumer of a REST framework might expect. Using Django REST
        # framework app will probably make this unnecessary.
        items = json.loads(json_data)
        converted_items = list()
        for obj in items:
            converted_items.append(_django_model_json_to_rest_json(obj))
        json_data = json.dumps(converted_items, sort_keys=True, indent=4)
        
    except TypeError:
        # Assume that TypeError is only thrown due to passing non-iterable to
        # django.core.serializers.serialize(). Probably not the best assumption
        # but good enough for a quick prototype.
        json_data = serialize('json', (model_or_models,), **options)

        # Django does special treatment of the Model serialization to preserve
        # it over the network, so we need to adjust the output to look more as
        # a consumer of a REST framework might expect. Using Django REST
        # framework app will probably make this unnecessary.
        items = json.loads(json_data)
        converted_item = _django_model_json_to_rest_json(items[0])
        json_data = json.dumps(converted_item, sort_keys=True, indent=4)

    return json_data


def deserialize_models(json_data, expect_single_object: bool=False, default_id: str='00000000-0000-0000-0000-000000000000'):
    """
    Deserialize a string containing either a JSON object that is a representation
    of a Django model object or a JSON array of such objects. They are
    decoded into Django model JSON and then deserialized into a series of
    DeserializedObject as per the typical call to django.core.serializer's
    deserialize function. By default, only a JSON array is allowed to be decoded;
    attempting to pass in a single JSON object will result in a ModelParseError
    being raised. The parse mode can be switched from array of objects to a
    single object by setting expect_single_object to True.

    Regardless of whether json_data contains a single opject or an array of
    objects, all objects within it must have the 'model' attribute.
    Failure to meet this will result in a ModelParseError being raised.

    If any object being parsed does not contain an ID attribute, it will be set
    to a default value prior to deserialization by Django. To set what this
    default use, give a value for default_id.

    :param expect_single_object: Set this to True to require the input to be a
    single JSON object instead of a JSON array of objects.
    :param default_id: What a parsed object will have its ID set to when it does
    not explicitly give one.
    :return: An iterator that returns DeserializedObject instances.
    :raises:
        ModelParseError: If expect_single_object is False (the default) and the
        json_data does not contain an array, or if expect_single_object is True
        and the json_data does not contain a JSON object. Additionally, this
        will be raised if any model object being deserialized is missing the
        required key 'model'.
    """

    loaded_json = json.loads(json_data)
    if expect_single_object:
        # we expect to have been sent a single object in json. Treat the loaded
        # json accordingly, but be ready to catch exceptions as input may be
        # from external source
        try:
            converted_obj = _rest_json_to_django_model_json(loaded_json, default_id)
        except KeyError as e:
            raise ModelParseError("Model JSON is not valid: " + str(e))
        except TypeError as e:
            raise ModelParseError("Model JSON cannot be {!s}; must be a JSON object at top level".format(type(loaded_json)))
        
        # Put in list because Django's serialize always produces a JSON array,
        # so we will match that prior to passing to deserialize.
        django_json = json.dumps(list(converted_obj))
    else:
        converted_items = list()
        # we expect to have been sent an array of objects in JSON. Treat the
        # loaded json accordingly, but be ready to catch exceptions as input may
        # be from external source
        for item in loaded_json:
            try:
                converted_obj = _rest_json_to_django_model_json(item, default_id)
            except KeyError as e:
                raise ModelParseError("Model JSON is not valid: " + str(e))
            except TypeError as e:
                raise ModelParseError("Model JSON cannot be {!s}; must be a JSON array at top level".format(type(loaded_json)))

            converted_items.append(item)
        django_json = json.dumps(converted_items)
    return deserialize('json', django_json)


def _django_model_json_to_rest_json(json_obj: dict) -> dict:
    """
    Convert a dict that is the result of decoding the output of Django's
    'serialize' function to generic json object(s) by applying transformations
    them. The field "pk"'s name is changed to be "id" and all attributes of the
    "fields" object are moved to be top-level attributes of each object, and the
    "fields" object itself is removed entirely.

    Note that if the Model has a field called 'model' explicitly defined
    on it, it may conflict with the Django-provided values in the output. The
    field value will overwrite it in that case.
    """

    if 'fields' not in json_obj or 'pk' not in json_obj or 'model' not in json_obj:
        raise KeyError("object is missing one or more of 'fields', 'pk', or 'model' attributes; was this created with a call to django.core.serializers.serialize?")
    
    json_obj['id'] = json_obj['pk']
    del json_obj['pk']
    
    for k in json_obj['fields']:
        if k == 'fields':
            # dont overwrite the structure we are currently iterating over
            # Will check for this post-iteration and move it up after everything
            # else has been if it exists
            continue
        json_obj[k] = json_obj['fields'][k]

    # check if we left behind a field called 'fields' during iteration:
    if 'fields' in json_obj['fields']:
        # one exists, and it will have been skipped during iteration.
        # use it to overwrite the old top-level 'fields' attribute.
        new_fields = json_obj['fields']['fields']
        json_obj['fields'] = new_fields
    else:
        # there is no field named 'fields' and iteration will have covered moving
        # everything. It is safe to delete the top-level 'fields' attribute.
        del json_obj['fields']

    return json_obj

def _rest_json_to_django_model_json(json_obj: dict, default_id: str='00000000-0000-0000-0000-000000000000') -> dict:
    """
    Convert a dict in typical 'REST'-ish format into one that is suitable for
    passing to django's deserialize function. See _django_model_json_to_rest_json
    for the transformations that are applied; this function applies the inverse
    tranformation, with the exception that the 'id' attribute is not required.

    If the received object does not have an ID, it is set to the default_id
    given.
    """

    if 'model' not in json_obj:
        raise KeyError("object is missing 'model' attribute")
    
    fields_dict = dict()
    for k in json_obj:
        if k == 'id' or k == 'model':
            continue
        fields_dict[k] = json_obj[k]
        del json_obj[k]
    
    json_obj['fields'] = fields_dict

    if 'id' in json_obj:
        json_obj['pk'] = json_obj['id']
        del json_obj['id']
    else:
        json_obj['pk'] = default_id

    return json_obj