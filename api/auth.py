from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Ici, vous validez le token et récupérez l'utilisateur
    # Pour simplifier, nous retournons un utilisateur fictif
    return {"username": "testuser"}