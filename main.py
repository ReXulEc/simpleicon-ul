import imp
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
import json
import webbrowser
import requests




class FfExtension(Extension): 

 
    def __init__(self):
        super(FfExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

   

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or str()
        querywithoutcaps = query.lower()
        x = requests.get('https://unpkg.com/simple-icons@7.4.0/icons/%s.svg' % querywithoutcaps)
        f = open('data.json')
        data = json.load(f)
        def find_item(arr, title):
            for item in arr:
                if item["title"] == title:
                    return item
            return None

        items = [
            ExtensionResultItem(
                icon = 'images/browser.svg',
                name = "SimpleIcon | Type somthing to search for an icon",
                description = 'example: "sp spotify"',
                on_enter=ExtensionCustomAction(query, keep_app_open=True)
            )
        ]

        if query == "":
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='SimpleIcon | Type somthing to search for an icon',
                    description='example: "sp spotify"',
                    on_enter=HideWindowAction()
                )
            ])
        elif x.status_code == 404:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='No icon found',
                    description='No icon found',
                    on_enter=HideWindowAction()
                )
            ])
        else:
            items = [
                ExtensionResultItem(
                    icon = 'images/icon.png',
                    name = event.get_argument().capitalize(),
                    description = "Click enter to open %s's icon." % event.get_argument(),
                    on_enter=ExtensionCustomAction(querywithoutcaps, keep_app_open=True)
                ),
                ExtensionResultItem(
                    icon = 'https://singlecolorimage.com/get/%s/400x400' % find_item(data["icons"], query.capitalize())["hex"],
                    name = "Primary Color : %s" % find_item(data["icons"], query.capitalize())["hex"],
                    description = "Click enter to copy primary color.",
                    on_enter=CopyToClipboardAction(find_item(data["icons"], query.capitalize())["hex"]),
                )
            ]

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_data() or str()
        querywithoutcaps = query.lower()
        webbrowser.open_new_tab('https://unpkg.com/simple-icons@7.4.0/icons/%s.svg' % querywithoutcaps)
        
        return RenderResultListAction([])

if __name__ == '__main__':
    FfExtension().run()