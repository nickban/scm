
from .models import Sample
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

import tempfile
from django.shortcuts import get_object_or_404, render

# 要使用这个插件，需要安装 cairo pango
# On Mac OS X using homebrew:
# brew install cairo
# brew install pango


def generate_pdf(request, pk):
    """Generate pdf."""
    # Model data
    sample = get_object_or_404(Sample, pk=pk)

    # Rendered
    uri = request.build_absolute_uri()
    html_string = render_to_string('sample/pdf.html', {'sample': sample})
    html = HTML(string=html_string, base_url=uri)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=sample_ditail.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response
