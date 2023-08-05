# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details
# http://www.gnu.org/licenses/gpl-3.0.txt

"""Torrent commands for the TUI"""

from ...logging import make_logger
log = make_logger(__name__)

from collections import abc

from ..base import torrent as base
from . import mixin
from .. import ExpectedResource
from ...utils import strcrop
from . import make_tab_title


class AddTorrentsCmd(base.AddTorrentsCmdbase,
                     mixin.polling_frenzy, mixin.make_request):
    provides = {'tui'}


class AnnounceTorrentsCmd(base.AnnounceTorrentsCmdbase,
                          mixin.make_request, mixin.select_torrents):
    provides = {'tui'}


class ListTorrentsCmd(base.ListTorrentsCmdbase,
                      mixin.select_torrents):
    provides = {'tui'}
    tui = ExpectedResource

    def make_tlist(self, tfilter, sort, columns):
        # Enforce 'marked' column
        if 'marked' not in columns:
            columns.insert(0, 'marked')

        def make_title_widget(text):
            return make_tab_title(text,
                                  'tabs.torrentlist.unfocused',
                                  'tabs.torrentlist.focused')

        from ...tui.torrent.tlist import TorrentListWidget
        tlistw = TorrentListWidget(tfilter=tfilter, sort=sort, columns=columns)
        tabid = self.tui.tabs.load(make_title_widget(tlistw.title), tlistw)

        def set_tab_title(text):
            self.tui.tabs.set_title(make_title_widget(text), position=tabid)
        tlistw.title_updater = set_tab_title

        return True


class ListFilesCmd(base.ListFilesCmdbase,
                   mixin.make_request, mixin.select_torrents, mixin.select_files):
    provides = {'tui'}
    tui = ExpectedResource
    srvapi = ExpectedResource

    async def make_flist(self, tfilter, ffilter, columns):
        if isinstance(tfilter, abc.Sequence) and len(tfilter) == 1:
            # tfilter is a torrent ID - resolve it to a name for the title
            response = await self.srvapi.torrent.torrents(tfilter, keys=('name',))
            title = strcrop(response.torrents[0]['name'], 30, tail='…')
        else:
            title = None

        # Enforce 'marked' column
        if 'marked' not in columns:
            columns.insert(0, 'marked')

        from ...tui.torrent.flist import FileListWidget
        flistw = FileListWidget(self.srvapi, tfilter, ffilter, columns, title=title)

        def make_title_widget(text):
            return make_tab_title(text,
                                  'tabs.filelist.unfocused',
                                  'tabs.filelist.focused')

        tabid = self.tui.tabs.load(make_title_widget(flistw.title), flistw)

        def set_tab_title(text):
            self.tui.tabs.set_title(make_title_widget(text), position=tabid)
        flistw.title_updater = set_tab_title

        return True


class ListPeersCmd(base.ListPeersCmdbase,
                   mixin.make_request, mixin.select_torrents):
    provides = {'tui'}
    tui = ExpectedResource
    srvapi = ExpectedResource

    async def make_plist(self, tfilter, pfilter, sort, columns):
        if isinstance(tfilter, abc.Sequence) and len(tfilter) == 1:
            # tfilter is a torrent ID - resolve it to a name for the title
            response = await self.srvapi.torrent.torrents(tfilter, keys=('name',))
            title = strcrop(response.torrents[0]['name'], 30, tail='…')
        else:
            title = None

        from ...tui.torrent.plist import PeerListWidget
        plistw = PeerListWidget(self.srvapi, tfilter=tfilter, pfilter=pfilter,
                                sort=sort, columns=columns, title=title)

        def make_title_widget(text):
            return make_tab_title(text,
                                  'tabs.peerlist.unfocused',
                                  'tabs.peerlist.focused')

        tabid = self.tui.tabs.load(make_title_widget(plistw.title), plistw)

        def set_tab_title(text):
            self.tui.tabs.set_title(make_title_widget(text), position=tabid)
        plistw.title_updater = set_tab_title

        return True


class MoveTorrentsCmd(base.MoveTorrentsCmdbase,
                      mixin.polling_frenzy, mixin.make_request, mixin.select_torrents):
    provides = {'tui'}


class PriorityCmd(base.PriorityCmdbase,
                  mixin.polling_frenzy, mixin.make_request, mixin.select_torrents, mixin.select_files):
    provides = {'tui'}


class RemoveTorrentsCmd(base.RemoveTorrentsCmdbase,
                        mixin.polling_frenzy, mixin.make_request, mixin.select_torrents):
    provides = {'tui'}


class StartTorrentsCmd(base.StartTorrentsCmdbase,
                       mixin.polling_frenzy, mixin.make_request, mixin.select_torrents):
    provides = {'tui'}


class StopTorrentsCmd(base.StopTorrentsCmdbase,
                      mixin.polling_frenzy, mixin.make_request, mixin.select_torrents):
    provides = {'tui'}


class VerifyTorrentsCmd(base.VerifyTorrentsCmdbase,
                        mixin.make_request, mixin.select_torrents):
    provides = {'tui'}
