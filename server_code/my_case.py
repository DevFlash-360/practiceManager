from ..app.models import * # noqa
import anvil.server
import anvil.secrets


PMAPP_API_ORIGIN = 'https://dd2scido6vqpf3xb.anvil.app/UFWI73RUL6AQM3I2K32OXEHW/_/api'


@anvil.server.http_endpoint('/my-case/auth', methods=['GET', 'POST'])
def auth(**params):
    print(f"method: {anvil.server.request.method}\n"
          "headers: {anvil.server.request.headers}\n"
          f"params: {params}\n")

    tenant_uid = params['state'] if params['state'] else None

    return anvil.server.HttpResponse(200, f'OK')
