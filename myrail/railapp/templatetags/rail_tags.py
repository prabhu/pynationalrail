from django import template

register = template.Library()

@register.tag
def service_link(parser, token):
    try:
        tag_name, service, crs, nextService = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly three arguments" % token.contents.split()[0]
    return ServiceLinkNode(service, crs, nextService)

class ServiceLinkNode(template.Node):
    
    def __init__(self, service, crs, nextService):
        self.service = template.Variable(service)
        self.crs = template.Variable(crs)
        self.nextService = template.Variable(nextService)
    
    def render(self, context):
        try:
            service = self.service.resolve(context)
            crs = self.crs.resolve(context)
            nextService = self.nextService.resolve(context)
            return '/s/?id=' + service.serviceID + '&crs=' + crs + '&nid=' + nextService.get(service.serviceID, '')
        except template.VariableDoesNotExist:
            return ''