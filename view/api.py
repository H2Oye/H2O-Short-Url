from flask import Blueprint, request, Response
from module import core, auxiliary, model, database_type
import config

API_APP = Blueprint('API_APP', __name__, url_prefix='/api')

@API_APP.get('/get_domain')
def getDomain() -> Response:
    result = [item.domain for item in model.Domain.query.all()]
    return core.GenerateResponse().success(result)

@API_APP.post('/generate')
def generate() -> Response:
    parameter = request.get_json()
    domain = parameter.get('domain')
    longUrl = parameter.get('longUrl')
    signature = parameter.get('signature')
    validDay = parameter.get('validDay', 0)
    if not domain or not longUrl:
        return core.GenerateResponse().error(110, '参数不能为空')
    elif not auxiliary.isUrl(longUrl):
        return core.GenerateResponse().error(110, 'longUrl需完整')
    elif type(validDay) != int:
        return core.GenerateResponse().error(110, 'validDay仅能为数字')
    elif validDay != 0:
        if validDay < 0 or validDay > 365:
            return core.GenerateResponse().error(110, 'validDay仅能填0~365,0代表永久')
    
    domainD = model.Domain.query.filter_by(domain=domain).first()
    if not domainD:
        return core.GenerateResponse().error(110, 'domain不存在')
    if config.AUTOMATIC:
        protocol = 'https'
    else:
        if database_type.Domain(domainD.protocol) == database_type.Domain.HTTP:
            protocol = 'http'
        else:
            protocol = 'https'
    
    if signature:
        if not signature.isdigit() and not signature.isalpha() and not signature.isalnum():
            return core.GenerateResponse().error(110, 'signature仅能为数字和字母')
        elif len(signature) < 1 or len(signature) > 5:
            return core.GenerateResponse().error(110, 'signature长度仅能为1~5')
        elif signature.lower() == 'api':
            return core.GenerateResponse().error(110, 'signature不能为api')
        elif signature.lower() == 'index':
            return core.GenerateResponse().error(110, 'signature不能为index')
        elif signature.lower() == 'query':
            return core.GenerateResponse().error(110, 'signature不能为query')
        elif model.Url.query.filter_by(domain_id=domainD.id, signature=signature).first():
            return core.GenerateResponse().error(110, 'signature已存在')

        url = model.Url(type_=database_type.Url.CUSTOM, domain_id=domainD.id, long_url=longUrl, valid_day=validDay, signature=signature)
        model.DB.session.add(url)
        model.DB.session.commit()
    else:
        url = model.Url.query.filter_by(domain_id=domainD.id, long_url=longUrl).first()
        if url:
            return core.GenerateResponse().success(f'{protocol}://{domain}/{url.signature}')
        
        url = model.Url(type_=database_type.Url.CUSTOM, domain_id=domainD.id, long_url=longUrl, valid_day=validDay)
        model.DB.session.add(url)
        model.DB.session.commit()

        signature = auxiliary.base62Encode(url.id)
        if model.Url.query.filter_by(domain_id=domainD.id, signature=signature).first():
            signature += 'a'
        url.signature = signature
        model.DB.session.commit()
    return core.GenerateResponse().success(f'{protocol}://{domain}/{signature}')

@API_APP.get('/get')
def get() -> Response:
    parameter = request.args
    domain = parameter.get('domain')
    signature = parameter.get('signature')
    if not domain or not signature:
        return core.GenerateResponse().error(110, '参数不能为空')

    domainD = model.Domain.query.filter_by(domain=domain).first()
    if not domainD:
        return core.GenerateResponse().error(110, 'shortUrl错误')
    url = model.Url.query.filter_by(domain_id=domainD.id, signature=signature).first()
    if not url:
        return core.GenerateResponse().error(110, 'shortUrl错误')
    
    return core.GenerateResponse().success({
        'longUrl': url.long_url,
        'validDay': url.valid_day,
        'count': url.count,
        'creationTimestamp': url.creation_timestamp
    })