from Systems.CBGP.Configuration import cbgp_feature_printer
from Systems.CBGP.Translation.router_translator import cbgp_translator
from test_runner import *


class CBGPRunner(TestRunner):

    def __init__(self, path, topo, system, router_features=None, cbgp_features=None, resource_conversion=None):
        super().__init__(path, topo, system, router_features)

        self.resource_conversion = resource_conversion
        self.cbgp_features = cbgp_features
        if self.cbgp_features is not None:
            self.last_cbgp_args = {cbgp_feature: -1 for cbgp_feature in self.cbgp_features}
        else:
            self.last_cbgp_args = None

    def translate_router_args(self, row_features):
        translator_features = {cbgp_translator[fl]: {} for fl in cbgp_translator}

        for (router, feature, arg) in row_features:
            for feature_list in cbgp_translator:
                if router.feature_list == feature_list:
                    translator_features[cbgp_translator[feature_list]][router, feature, arg] = row_features[
                        router, feature, arg]

        router_config = {}

        for translator in translator_features:
            t = translator.translate_config(translator_features[translator],
                                            self.topo.routers,
                                            self.router_features,
                                            **self.resource_conversion)
            router_config = {**t, **router_config}
        return router_config

    def set_router_args(self, row_features):

        router_config = self.translate_router_args(row_features)
        router_configurator.set_args_from_translation(router_config)

    def run_test(self, cur_features, cur_args=None):
        """
        Run a test case with specified features and args
        :param cur_features: Features which should be enabled in this test case
        :param cur_args: Arguments for the enabled features, if None the last args are used instead
        :return: Result of the test: 0 if comparison ok, 1 for difference, 2 for sut crash, 3 for timeout
        """
        logger = logging.getLogger('network-testing')
        logger.info(f'Running C-BGP test case with features {str_repr(cur_features)}')

        if cur_args is None:
            cur_args = self.last_cbgp_args

        router_config = self.translate_router_args(filter_dict(cur_features, cur_args))
        router_features = [f for f in self.router_features if router_config[f] != -1]
        router_configurator.set_args_from_translation(router_config)
        cbgp_feature_printer.generate_cbgp_config(f'{self.path}test{self.test_num}/', self.topo, filter_dict(cur_features, cur_args))

        self.last_cbgp_args = cur_args

        return super().run_test(router_features, router_config)
