## READ ME

use python
use REST
sqlite3

use authentication rest_toke_auth

user_types:
- noob
- elite
- admin

models:
- user
- wallet

endpoints:
- signup
- login
- fund wallet in different currency:
    - approve funding
- withdraw funds

- create wallet
- fund wallet:
    - create wallet in currency
- withdraw funds:
    - if elite - withdraw funds from currency wallet
    - if no funds, check main account and withdraw
- cannot change main currency

admin:
- fund wallet for users
- chnage main currency of user
- approve wallet funding for noob
- promote or demote users