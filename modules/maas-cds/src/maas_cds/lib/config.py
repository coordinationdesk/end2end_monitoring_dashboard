def get_good_threshold_config_from_value(config, value):

    ordered_keys = list(config.keys())

    ordered_keys.sort(reverse=True)

    for key in ordered_keys:
        if value >= key:
            return (key, config[key])
    return (None, None)
