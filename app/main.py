from app.service import app
from app.configuration import SERVICE_HOSTNAME, SERVICE_PORT, SERVICE_DEBUG


if __name__ == "__main__":
    app.run(host=SERVICE_HOSTNAME, port=SERVICE_PORT, debug=SERVICE_DEBUG)
