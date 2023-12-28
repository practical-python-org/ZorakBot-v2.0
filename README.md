# Zorak v2.0

ZorakBot is the House bot of the Practical Python discord server.

Its purpose is to moderate, log, and provide necessary features that the community deems worthy. 
Anyone from our community is welcome to join us in developing the bot. 
Zorak uses Discord.py with cogged commands, listeners and events. 
All of this is wrapped tightly around a Postgres Database.


Checklist:
- [ ] Full server logging
- [ ] Admin commands
- [ ] Spam prevention
- [ ] Raid protection
- [ ] A points system
- [ ] Fun Commands
- [ ] Reaction roles
- [ ] Music functions

      
## File Overview
- **db**
  - database.py
  - **DB schema** - A visual overview of the database
- **src**
  -  **/cogs**
    - **_templates** - Template cogs, for your development ease
    - **admin** - Admin commands
    - **fun** - Fun commands
    - **logging** - All logging cogs 
    - **tools** - utilities, auto-features, random...
- logger.py
- main.py
- .env
      
      
