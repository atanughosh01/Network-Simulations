## Simulation Guide

 * First, in a terminal window, start the server by saying `python3 server.py`
 * Then, in a different terminal window, start a client by saying `python3 client.py`
 * You can open as many clients as you want, by simply running `python3 client.py` on separate terminal windows.
 * You need to enter your name, and then enter the server address and port no. which is **127.0.0.1** and **5050** .
 * **Every signup/login is as a guest by default**.
 * Now, you can execute **GET** and **PUT** , as required in any order.

    ```
        GET city
        PUT city Kolkata
    ```
 
 * To change into manager mode, type `sudo-su-manager` and enter the password `chmon#manager` .
 * As a manager, you can **GET** and **PUT** by following the command with the username, eg:

    ```
        GET [username] city 
        PUT [username] city Kolkata
    ```

* Type `logout` to end the client session.
