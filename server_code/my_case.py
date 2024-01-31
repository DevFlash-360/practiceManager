from .app.models import * # noqa
import anvil.server
import anvil.secrets


PMAPP_API_ORIGIN = 'https://dd2scido6vqpf3xb.anvil.app/UFWI73RUL6AQM3I2K32OXEHW/_/api'


@anvil.server.http_endpoint('/my-case/auth', methods=['GET', 'POST'])
def auth(**params):
    print(f"method: {anvil.server.request.method}\n"
          f"headers: {anvil.server.request.headers}\n"
          f"params: {params}\n")

    tenant_uid = params.get('state', None)

    return anvil.server.HttpResponse(200, f'OK')
