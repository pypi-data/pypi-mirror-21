import unittest
import numpy as np
import scipy.stats as st
from os import path, getcwd

from ..analysis.analysis import analyze, NoDataError


class MyTestCase(unittest.TestCase):

    _seed = 987654321

    @property
    def save_path(self):
        if getcwd().split('/')[-1] == 'test':
            return './images/'
        elif getcwd().split('/')[-1] == 'sci_analysis':
            if path.exists('./setup.py'):
                return './sci_analysis/test/images/'
            else:
                return './test/images/'
        else:
            './'

    def test_100_catch_no_data_1_array(self):
        """Catch the case where no data is passed"""
        self.assertRaises(NoDataError, lambda: analyze([]))

    def test_101_catch_no_data_None(self):
        """Catch the case where None is passed"""
        self.assertRaises(ValueError, lambda: analyze(None))

    def test_102_catch_xdata_no_iterable(self):
        """Catch the case where xdata is not iterable"""
        self.assertRaises(TypeError, lambda: analyze(1))

    def test_103_catch_more_than_2_data_args(self):
        """Catch the case where more than 2 data arguments are given"""
        self.assertRaises(ValueError, lambda: analyze(st.norm.rvs(size=10), st.norm.rvs(size=10), st.norm.rvs(size=10)))

    def test_104_ttest_large_default(self):
        """Perform an analysis on a large sample using the ttest"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.norm.rvs(size=100)
        self.assertEqual(analyze([input_1_array, input_2_array], debug=True,
                                 save_to='{}test_analyze_104'.format(self.save_path)),
                         ['Oneway', 'TTest'])

    def test_105_ttest_small_default(self):
        """Perform an analysis on a small sample using the ttest"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=10)
        input_2_array = st.norm.rvs(size=10)
        self.assertEqual(analyze([input_1_array, input_2_array], debug=True,
                                 save_to='{}test_analyze_105'.format(self.save_path)),
                         ['Oneway', 'TTest'])

    def test_106_ttest_large_group(self):
        """Perform an analysis on a large sample using the ttest with set group names"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.norm.rvs(size=100)
        self.assertEqual(analyze([input_1_array, input_2_array],
                                 groups=['Test 1', 'Test 2'],
                                 debug=True,
                                 save_to='{}test_analyze_106'.format(self.save_path)),
                         ['Oneway', 'TTest'])

    def test_107_ttest_large_dict(self):
        """Perform an analysis on a large sample using the ttest with set dict"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.norm.rvs(size=100)
        self.assertEqual(analyze({'dTest 1': input_1_array, 'dTest 2': input_2_array},
                                 debug=True,
                                 save_to='{}test_analyze_107'.format(self.save_path)),
                         ['Oneway', 'TTest'])

    def test_108_ttest_xlabel_ylabel(self):
        """Perform an analysis on a large sample using the ttest with labels set"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.norm.rvs(size=100)
        self.assertEqual(analyze([input_1_array, input_2_array],
                                 title='Labels test',
                                 xname='X Test',
                                 yname='Y Test',
                                 debug=True,
                                 save_to='{}test_analyze_108'.format(self.save_path)),
                         ['Oneway', 'TTest'])

    def test_109_mannwhitney_default(self):
        """Perform an analysis on a non-normal data set using the Mann Whitney test"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.weibull_min.rvs(1.2, size=100)
        self.assertEqual(analyze([input_1_array, input_2_array],
                                 title='MannWhitney Default',
                                 debug=True,
                                 save_to='{}test_analyze_109'.format(self.save_path)),
                         ['Oneway', 'MannWhitney'])

    def test_110_mannwhitney_groups(self):
        """Perform an analysis on a non-normal data set using the Mann Whitney test"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.weibull_min.rvs(1.2, size=100)
        self.assertEqual(analyze([input_1_array, input_2_array],
                                 groups=['Test 1', 'Test 2'],
                                 title='MannWhitney Groups',
                                 debug=True,
                                 save_to='{}test_analyze_110'.format(self.save_path)),
                         ['Oneway', 'MannWhitney'])

    def test_111_mannwhitney_groups(self):
        """Perform an analysis on a non-normal data set using the Mann Whitney test"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.weibull_min.rvs(1.2, size=100)
        self.assertEqual(analyze({'dTest 1': input_1_array, 'dTest 2': input_2_array},
                                 title='MannWhitney Dict',
                                 debug=True,
                                 save_to='{}test_analyze_111'.format(self.save_path)),
                         ['Oneway', 'MannWhitney'])

    def test_112_twosampleks_default(self):
        """Perform an analysis on a small bi-modal data set using the twosample ks test"""
        np.random.seed(self._seed)
        input_1_array = np.append(st.norm.rvs(0, 1, size=10), st.norm.rvs(10, 1, size=10))
        input_2_array = np.append(st.norm.rvs(0, 1, size=10), st.norm.rvs(10, 1, size=10))
        self.assertEqual(analyze([input_1_array, input_2_array],
                                 title='TwoSampleKSTest Default',
                                 debug=True,
                                 save_to='{}test_analyze_112'.format(self.save_path)),
                         ['Oneway', 'TwoSampleKSTest'])

    def test_113_twosampleks_groups(self):
        """Perform an analysis on a small bi-modal data set using the twosample ks test"""
        np.random.seed(self._seed)
        input_1_array = np.append(st.norm.rvs(0, 1, size=10), st.norm.rvs(10, 1, size=10))
        input_2_array = np.append(st.norm.rvs(0, 1, size=10), st.norm.rvs(10, 1, size=10))
        self.assertEqual(analyze([input_1_array, input_2_array],
                                 groups=['Group 1', 'Group 2'],
                                 title='TwoSampleKSTest Groups',
                                 debug=True,
                                 save_to='{}test_analyze_113'.format(self.save_path)),
                         ['Oneway', 'TwoSampleKSTest'])

    def test_114_twosampleks_dict(self):
        """Perform an analysis on a small bi-modal data set using the twosample ks test"""
        np.random.seed(self._seed)
        input_1_array = np.append(st.norm.rvs(0, 1, size=10), st.norm.rvs(10, 1, size=10))
        input_2_array = np.append(st.norm.rvs(0, 1, size=10), st.norm.rvs(10, 1, size=10))
        self.assertEqual(analyze({'dGroup 1': input_1_array, 'dGroup 2': input_2_array},
                                 title='TwoSampleKSTest Dict',
                                 debug=True,
                                 save_to='{}test_analyze_114'.format(self.save_path)),
                         ['Oneway', 'TwoSampleKSTest'])

    def test_115_ttest_name_categories_default(self):
        """Perform an analysis on a large sample using the ttest with labels set"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.norm.rvs(size=100)
        self.assertEqual(analyze([input_1_array, input_2_array],
                                 title='Labels test 2',
                                 categories='X Test',
                                 name='Y Test',
                                 debug=True,
                                 save_to='{}test_analyze_115'.format(self.save_path)),
                         ['Oneway', 'TTest'])

    def test_116_ttest_name_categories_groups(self):
        """Perform an analysis on a large sample using the ttest with labels set"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.norm.rvs(size=100)
        self.assertEqual(analyze([input_1_array, input_2_array],
                                 groups=['Group 1', 'Group 2'],
                                 title='Labels test 2 Groups',
                                 categories='X Test',
                                 name='Y Test',
                                 debug=True,
                                 save_to='{}test_analyze_116'.format(self.save_path)),
                         ['Oneway', 'TTest'])

    def test_117_ttest_name_categories_dict(self):
        """Perform an analysis on a large sample using the ttest with labels set"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.norm.rvs(size=100)
        self.assertEqual(analyze({'dGroup 1': input_1_array, 'dGroup 2': input_2_array},
                                 title='Labels test Dict',
                                 categories='X Test',
                                 name='Y Test',
                                 debug=True,
                                 save_to='{}test_analyze_117'.format(self.save_path)),
                         ['Oneway', 'TTest'])

    def test_118_ttest_alpha(self):
        """Perform an analysis on a large sample using the ttest with alpha 0.02"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.norm.rvs(size=100)
        self.assertEqual(analyze([input_1_array, input_2_array],
                                 title='Alpha 0.02',
                                 alpha=0.02,
                                 debug=True,
                                 save_to='{}test_analyze_118'.format(self.save_path)),
                         ['Oneway', 'TTest'])

    def test_119_ttest_no_nqp(self):
        """Perform an analysis on a large sample using the ttest without a nqp"""
        np.random.seed(self._seed)
        input_1_array = st.norm.rvs(size=100)
        input_2_array = st.norm.rvs(size=100)
        self.assertEqual(analyze([input_1_array, input_2_array],
                                 title='No NQP',
                                 nqp=False,
                                 debug=True,
                                 save_to='{}test_analyze_119'.format(self.save_path)),
                         ['Oneway', 'TTest'])

    def test_120_bivariate_default(self):
        """Perform a correlation on two data sets with default settings"""
        np.random.seed(self._seed)
        input_x_array = st.weibull_min.rvs(2, size=200)
        input_y_array = np.array([x + st.norm.rvs(0, 0.5, size=1) for x in input_x_array])
        self.assertEqual(analyze(input_x_array, input_y_array,
                                 debug=True,
                                 save_to='{}test_analyze_120'.format(self.save_path)),
                         ['Bivariate'])

    def test_121_bivariate_xname_yname(self):
        """Perform a correlation on two data sets with labels set"""
        np.random.seed(self._seed)
        input_x_array = st.weibull_min.rvs(2, size=200)
        input_y_array = np.array([x + st.norm.rvs(0, 0.5, size=1) for x in input_x_array])
        self.assertEqual(analyze(input_x_array, input_y_array,
                                 xname='X Test',
                                 yname='Y Test',
                                 title='Labels Test',
                                 debug=True,
                                 save_to='{}test_analyze_121'.format(self.save_path)),
                         ['Bivariate'])

    def test_122_bivariate_alpha(self):
        """Perform a correlation on two data sets with alpha set to 0.02"""
        np.random.seed(self._seed)
        input_x_array = st.weibull_min.rvs(2, size=200)
        input_y_array = np.array([x + st.norm.rvs(0, 0.5, size=1) for x in input_x_array])
        self.assertEqual(analyze(input_x_array, input_y_array,
                                 alpha=0.02,
                                 title='Alpha Test',
                                 debug=True,
                                 save_to='{}test_analyze_122'.format(self.save_path)),
                         ['Bivariate'])

    def test_123_distribution_default(self):
        """Perform a distribution analysis with default settings"""
        np.random.seed(self._seed)
        input_array = st.norm.rvs(size=200)
        self.assertEqual(analyze(input_array,
                                 debug=True,
                                 save_to='{}test_analyze_123'.format(self.save_path)),
                         ['Distribution', 'NormTest'])

    def test_124_distribution_label(self):
        """Perform a distribution analysis with label set"""
        np.random.seed(self._seed)
        input_array = st.norm.rvs(size=200)
        self.assertEqual(analyze(input_array,
                                 name='Test',
                                 title='Label Test',
                                 debug=True,
                                 save_to='{}test_analyze_124'.format(self.save_path)),
                         ['Distribution', 'NormTest'])

    def test_125_distribution_population(self):
        """Perform a distribution analysis with population set"""
        np.random.seed(self._seed)
        input_array = st.norm.rvs(size=200)
        self.assertEqual(analyze(input_array,
                                 sample=False,
                                 title='Population Stats',
                                 debug=True,
                                 save_to='{}test_analyze_125'.format(self.save_path)),
                         ['Distribution', 'NormTest'])

    def test_126_distribution_cdf(self):
        """Perform a distribution analysis with cdf"""
        np.random.seed(self._seed)
        input_array = st.norm.rvs(size=200)
        self.assertEqual(analyze(input_array,
                                 cdf=True,
                                 title='CDF Test',
                                 debug=True,
                                 save_to='{}test_analyze_126'.format(self.save_path)),
                         ['Distribution', 'NormTest'])

    def test_127_distribution_fit_norm_default(self):
        """Perform a distribution analysis with normal dist KSTest"""
        np.random.seed(self._seed)
        input_array = st.norm.rvs(size=200)
        self.assertEqual(analyze(input_array,
                                 distribution='norm',
                                 fit=True,
                                 title='Norm Fit',
                                 debug=True,
                                 save_to='{}test_analyze_127'.format(self.save_path)),
                         ['Distribution', 'KSTest'])

    def test_128_distribution_fit_norm_alpha(self):
        """Perform a distribution analysis with normal dist KSTest and alpha 0.02"""
        np.random.seed(self._seed)
        input_array = st.norm.rvs(size=200)
        self.assertEqual(analyze(input_array,
                                 distribution='norm',
                                 fit=True,
                                 alpha=0.02,
                                 title='Alpha 0.02',
                                 debug=True,
                                 save_to='{}test_analyze_128'.format(self.save_path)),
                         ['Distribution', 'KSTest'])


if __name__ == '__main__':
    unittest.main()
