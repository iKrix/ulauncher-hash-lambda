import hashlib
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction


class Hash2Extension(Extension):
    def __init__(self):
        super(Hash2Extension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        argument = (event.get_argument() or '').encode('utf-8')
        keyword = event.get_keyword()

        # Find the keyword id using the keyword (since the keyword can be changed by users)
        for kwId, kw in extension.preferences.iteritems():
            if kw == keyword:
                keywordId = kwId

        # Show the algorithm specified as keyword, or all if the keyword was "hash"
        algos = hashlib.algorithms_available if keywordId == 'hash' else [keywordId]

        # credits: https://stackoverflow.com/a/48283398
        marker = set()
        unique = [not marker.add(x.lower()) and x for x in algos if x.lower() not in marker]
        unique.sort()

        for algo in unique:
            h = hashlib.new(algo)
            h.update(argument)
            hash = h.hexdigest()
            items.append(
                ExtensionResultItem(icon='icon.png', name=hash, description=algo.upper(), on_enter=CopyToClipboardAction(hash),
                                    highlightable=True))

        return RenderResultListAction(items)


if __name__ == '__main__':
    Hash2Extension().run()
