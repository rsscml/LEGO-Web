# -*- encoding: utf-8 -*-

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render

from databricks_cli.sdk.api_client import ApiClient
from databricks_cli.dbfs.api import DbfsApi
from databricks_cli.dbfs.dbfs_path import DbfsPath
import pandas as pd

DATABRICKS_HOST = "https://adb-3287475818480689.9.azuredatabricks.net/"
DATABRICKS_TOKEN = "dapi9c2d29eb74a2bd3f0955ead5b039a690"
api_client = ApiClient(host = DATABRICKS_HOST, token = DATABRICKS_TOKEN)


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def tables_data(request):
    dbfs_source_file_path = 'dbfs:/mnt/adls/MPF/Alternate_Currency_Keys_Aug.csv'
    local_file_download_path = './mpf_dataset.csv'
    dbfs_api  = DbfsApi(api_client)
    dbfs_path = DbfsPath(dbfs_source_file_path)
    dbfs_api.get_file(dbfs_path, local_file_download_path, overwrite = True)
    data = pd.read_csv(local_file_download_path).head(5)

    context = {
    "data":data,
    "data1":{
    'GLICode': data['GLI Code'],
    'Country': data['Country'],
    'Incoterm': data['Incoterm'],
    'EU001': data['EU001 OC'],
    'DS': data['DS OC'],
    'UOM': data['UOM Macro'],}
    }
    return render(request, "home/tables-data.html", context)