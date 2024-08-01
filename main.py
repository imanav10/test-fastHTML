from fasthtml.common import *

app,rt = fast_app()

@rt('/')
def get(): return Titled("Comparison", Div(H1('Indepth performance comparison for React vs FastHTML vs GO (Server Side)'), hx_get="/change"))

serve()