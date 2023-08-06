Copyright (c) 2017 Jose Diaz-Gonzalez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description: python-slack-tunes
        --------------------
        
        send slack music notifications from itunes or spotify
        
        Requirements
        ============
        
        - OS X
        - iTunes or Spotify
        
        Installation
        ============
        
        Using PIP via PyPI::
        
            pip install slack-tunes
        
        Using PIP via Github::
        
            pip install git+https://github.com/josegonzalez/python-slack-tunes.git#egg=slack-tunes
        
        Usage
        =====
        
        Export a ``SLACK_API_TOKEN``, as shown on their `tokens page <https://get.slack.help/hc/en-us/articles/215770388-Create-and-regenerate-API-tokens>`_, and then execute the binary:
        
        .. code-block:: shell
        
            export SLACK_API_TOKEN="YOUR_TOKEN"
            slack-tunes
        
        Slack tunes will run in the foreground, and can be terminated at any time. It will update the status at most every 10 seconds, and will clear your status if no music is playing.
        
        
        You can also specify multiple tokens via comma-delimiter. This is useful for notifying multiple slack teams.
        
        .. code-block:: shell
        
            export SLACK_API_TOKEN="YOUR_TOKEN,YOUR_OTHER_TOKEN"
            slack-tunes
        
        .. image:: https://cdn.rawgit.com/josegonzalez/python-slack-tunes/2383034e/demo.png
            :width: 1010px
            :align: center
            :height: 382px
            :alt: demo of slack-tunes output
        
Platform: UNKNOWN
Classifier: Development Status :: 5 - Production/Stable
Classifier: Topic :: System :: Archiving :: Backup
Classifier: License :: OSI Approved :: MIT License
Classifier: Programming Language :: Python :: 2.6
Classifier: Programming Language :: Python :: 2.7
