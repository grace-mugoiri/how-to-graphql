import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Link, Vote

class LinkFilter(django_filters.FilterSet): #relay allows you to use django-filter for filtering data
    class Meta:
        model = Link
        fields = ["url", "description"]
    
class LinkNode(DjangoObjectType): #data is exposed in Node, so for the links must be created
    class Meta:
        model = Link
        interfaces = (graphene.relay.Node, ) #each node implemenents interface with unique id

class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (graphene.relay.Node, )

class RelayQuery(graphene.ObjectType):
    relay_link = graphene.relay.Node.Field(LinkNode) #uses the linknode with relaylink field inside new query
    relay_links = DjangoFilterConnectionField(LinkNode, filterset_class=LinkFilter) #defines the relaylink field as a connection, which implements the pagination structure

class RelayCreateLink(graphene.relay.ClientIDMutation):
    link = graphene.Field(LinkNode)
    
    class Input:
        url = graphene.String()
        description = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None
        link = Link(
            url = input.get("url"),
            description = input.get("description"),
            posted_by = user,
        )
        link.save()
    
        return RelayCreateLink(link=link)

class RelayMutation(graphene.AbstractType):
    relay_create_link = RelayCreateLink.Field()