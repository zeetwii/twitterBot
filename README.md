# TwitterBot

This is a python based twitter chatbot that will auto respond to direct messages with a quick reply menu to allow for rapidly deployable simple support capabilities.  

To run the chatbot, only two dependencies are needed:
- [PyYAML](https://pyyaml.org/wiki/PyYAML) : Needed to parse the config and options files
- [Tweepy](https://docs.tweepy.org/en/stable/install.html) : Needed to use the Twitter API in Python

You will also need to get an API key via making a twitter developer account.  This is a fairly straightforward process that can be done [here](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api).  Note that the current way twitter does API permissions are for read, read and write, or read and write and direct message.  Because we are going to be using the direct message feature, you need to make your key with the third privilege set, even though we are not actually reading or sending tweets.  

