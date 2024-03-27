from flask import Blueprint, render_template, request, Response, redirect
from module import model, auxiliary
import datetime

PAGE_APP = Blueprint('PAGE_APP', __name__)

@PAGE_APP.get('/generate')
@PAGE_APP.get('/index')
@PAGE_APP.get('/')
def generate() -> str:
    return render_template(
        'generate.html',
        title=model.Core.query.filter_by(name='title').first().content,
        keyword=model.Core.query.filter_by(name='keyword').first().content,
        description=model.Core.query.filter_by(name='description').first().content,
        nowYear=datetime.datetime.now().year
    )

@PAGE_APP.get('/query')
def query() -> str:
    return render_template(
        'query.html',
        title=model.Core.query.filter_by(name='title').first().content,
        keyword=model.Core.query.filter_by(name='keyword').first().content,
        description=model.Core.query.filter_by(name='description').first().content,
        nowYear=datetime.datetime.now().year
    )

@PAGE_APP.route('/<signature>', methods=['GET', 'POST'])
@PAGE_APP.route('/<signature>/', methods=['GET', 'POST'])
def shortUrlRedirect(signature) -> Response:
    domain = model.Domain.query.filter_by(domain=request.host).first()
    if not domain:
        return redirect(request.host_url)
    url = model.Url.query.filter_by(domain_id=domain.id, signature=signature).first()
    if not url:
        return redirect(request.host_url)

    validDay = url.valid_day
    if validDay != 0:
        validDayTimestamp = validDay * 60 * 60 * 24
        expireTimestamp = url.creation_timestamp + validDayTimestamp
        if auxiliary.getTimestamp() > expireTimestamp:
            model.DB.session.delete(url)
            return redirect(request.host_url)

    url.count += 1
    model.DB.session.commit()
    return redirect(url.long_url)