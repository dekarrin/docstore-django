from django.core.serializers import serialize

def serialize_models(model_or_models):
    """
    Serialize a django Model or an iterable of Models to a JSON string. If a
    single non-iterable Model is passed in, a string containing that Model's
    JSON representation is returned; otherwise, a string containing a JSON list
    with all the provided Models's JSON represntations is returned.
    """

    try:
        json_data = serialize('json', model_or_models)
    except TypeError:
        # Assume that TypeError is only thrown due to passing non-iterable to
        # django.core.serializers.serialize(). Probably not the best assumption
        # but good enough for a quick prototype.
        json_data = serialize('json', (model_or_models,))

        # This funkiness is bc we should probably be using the REST framework;
        # however, we are on a deadline and this is a prototype. For future,
        # recommend looking at REST framework serialization
        json_data = json_data[1:-1].strip()  # chop off list markers

    return json_data