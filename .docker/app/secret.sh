# /bin/bash
echo SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe())")