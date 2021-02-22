import random


def set_args_from_params(params):

    for (router, feature, arg) in params:

        feature_list = router.feature_list

        if params[router, feature, arg] == -1:
            continue

        if feature in feature_list.router_features:
            args = router.get_possible_args()[feature][params[router, feature, arg]]
        elif feature in feature_list.filter_features:
            args = (*arg, *router.get_possible_args()[feature][params[router, feature, arg]])
        else:
            args = (arg, *router.get_possible_args()[feature][params[router, feature, arg]])
        router.features[feature, arg] = args


def set_args_from_translation(params):

    for (router, feature, arg) in params:

        feature_list = router.feature_list

        if params[router, feature, arg] == -1:
            continue

        if feature in feature_list.router_features:
            args = params[router, feature, arg]
        elif feature in feature_list.filter_features:
            args = (*arg, *params[router, feature, arg])
        else:
            args = (arg, *params[router, feature, arg])
        router.features[feature, arg] = args


def set_args(fs):
    for (router, feature, arg) in fs:

        feature_list = router.feature_list

        if (feature, arg) in router.enabled_features:
            continue

        if feature in feature_list.router_features:
            args = random.choice(router.get_possible_args()[feature])
        elif feature in feature_list.filter_features:
            args = (*arg, *random.choice(router.get_possible_args()[feature]))
        else:
            args = (arg, *random.choice(router.get_possible_args()[feature]))
        router.features[feature, arg] = args


def enable_features(router_configs, fs):
    config_modes = {}
    for router_name in router_configs:
        config_modes[router_name] = {}
    exit_mode = {}

    for (router, feature, arg) in fs:

        config_printer = router.config_printer

        config_mode = config_printer.config_mode(router, feature, arg)

        args = router.features[feature, arg]
        c = config_printer.feature_config[feature](*args)

        if config_mode in config_modes[router.name]:
            config_modes[router.name][config_mode].append(c)
        else:
            config_modes[router.name][config_mode] = [c]

        exit_mode[config_mode] = config_printer.exit_config_mode(feature)
        router.enabled_features[feature, arg] = args

    for router_name in config_modes:
        for config_mode in sorted(config_modes[router_name], reverse=True):
            router_configs[router_name].extend(list(config_mode))
            router_configs[router_name].extend(config_modes[router_name][config_mode])
            router_configs[router_name].extend(exit_mode[config_mode])


def disable_features(router_configs, fs):
    config_modes = {}
    for router_name in router_configs:
        config_modes[router_name] = {}
    exit_mode = {}

    for (router, feature, arg) in fs:

        config_printer = router.config_printer

        if (feature, arg) in router.enabled_features:

            config_mode = config_printer.config_mode(router, feature, arg)

            args = router.enabled_features[feature, arg]
            c = config_printer.feature_disable[feature](*args)

            if config_mode in config_modes[router.name]:
                config_modes[router.name][config_mode].append(c)
            else:
                config_modes[router.name][config_mode] = [c]

            exit_mode[config_mode] = config_printer.exit_config_mode(feature)
            router.enabled_features.pop((feature, arg))

    for router_name in config_modes:
        for config_mode in sorted(config_modes[router_name], reverse=True):
            router_configs[router_name].extend(list(config_mode))
            router_configs[router_name].extend(config_modes[router_name][config_mode])
            router_configs[router_name].extend(exit_mode[config_mode])
