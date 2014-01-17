function tagExternalLink(link)
{
    if (link.hostname != window.location.hostname)
    {
        $(link).attr('target', '_blank');
    }
}
