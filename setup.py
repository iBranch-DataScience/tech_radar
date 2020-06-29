import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='scraping_scheduler',
    version='0.0.1',
    description='Python scraping scheduler',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='scrape scheduler',
    install_requires=[],
    packages=setuptools.find_packages(),
    author='Jian Jian',
    author_email='jjian03@syr.edu',
    url='https://github.com/iBranch-DataScience/scraping_scheduler',
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable'
        'Development Status :: 4 - Beta',  # 当前开发进度等级（测试版，正式版等）
        'Intended Audience :: Developers',  # 模块适用人群
        'Topic :: Software Development :: Code Generators',  # 给模块加话题标签
        'License :: Freely Distributable, Public Domain (Creative Commons Attribution 4.0 International Public License (see LICENSE file)',  # 模块的license

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={  # 项目相关的额外链接
        'Blog': 'https://ibranch.fun',
    },
)
