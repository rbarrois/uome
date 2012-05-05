# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois


"""Store a local copy of a remote database, with synchronization of local changes.

Provides:
- Configurable conflict resolution
- Custom remote access

The only constraints is that each object, local or remote, has a globally unique identifier.

Missing features:
    - Merging values
    - Detection of objects added both locally and remotely
"""

import copy

class Change(object):
    
    MODE_LOCAL = 'local'
    MODE_REMOTE = 'remote'
    MODE_SKIP = 'skip'

    ACTION_ADD_REMOTE = 'add'
    ACTION_UPDATE_REMOTE = 'update'
    ACTION_SKIP = 'skip'
    ACTION_NONE = 'nothing'

    def __init__(self, key, previous, local, remote):
        self.key = key
        self.previous = previous
        self.local = local
        self.remote = remote
        self.resolution = None

    def has_conflict(self):
        if self.local == self.remote:
            return False

        elif self.previous is None:
            # Locally added
            return False

        elif self.local != self.previous:
            # Local changed, did remote change too?
            return self.remote != self.previous

        else:
            # Remote changed
            return False

    def resolve(self, mode=None):
        """Return the action to take and resolved local value."""
        if self.has_conflict() and mode is None:
            raise ResolutionNeeded()

        elif mode == self.MODE_SKIP:
            return (self.ACTION_SKIP, self.local)

        if self.previous is None:
            # New local value, add to remote
            return (self.ACTION_ADD_REMOTE, self.local)

        elif self.local == self.remote:
            # No change
            return (self.ACTION_NONE, self.previous)

        elif self.local == self.previous:
            # Remote changed
            return (self.ACTION_NONE, self.remote)

        elif self.remote == self.previous:
            # Local change
            if self.local is None:
                return (self.ACTION_REMOVE_REMOTE, None)
            else:
                return (self.ACTION_UPDATE_REMOTE, self.local)

        elif mode == self.MODE_LOCAL:
            # Both changed, keep local
            if self.local is None:
                return (self.ACTION_REMOVE_REMOTE, None)
            else:
                return (self.ACTION_UPDATE_REMOTE, self.local)

        else:
            # Both changed, keep remote
            return (self.ACTION_NONE, self.remote)

    def __repr__(self):
        return '%s: %r to %s / %r' % (self.key, self.previous, self.local, self.remote)


class BaseStore(object):
    """Stores objects and handles addition/deletion/updates.

    Attributes:
        connector: RemoteConnector, handles reading/writing/deleting to the
            remote
        original: dict mapping an object key to its last synced value
        added: dict mapping an object key to its value for newly added objects
        deleted: set of keys of removed objects
        modified: dict mapping an object key to its updated value
    """

    def __init__(self, connector):
        self.connector = connector
        self.original = {}

        self.added = {}
        self.deleted = set()
        self.modified = {}

    def __getitem__(self, key):
        """Retrieve an item from the store, by key.

        Returns either:
        - The currently modified value, if any
        - The added value, if any
        - A *copy* of the original value
        """
        if key in self.modified:
            return self.modified[key]
        elif key in self.added:
            return self.added[key]
        else:
            return copy.copy(self.original[key])

    def __setitem__(self, key, value):
        """Update or add an item to the store.

        - If the value is equal to the original one, remove all modifications
        - If the value differs from the original one, update the list of
            modifications
        - If the key didn't exist, store the value in the list of additions.
        """
        if key in self.modified:
            if value == self.original[value]:
                del self.modified[key]
            else:
                self.modified[key] = value

        elif key in self.deleted:
            del self.deleted[key]
            if value != self.original[value]:
                self.modified[key] = value

        elif key in self.added:
            self.added[key] = value

        elif key in self.original:
            if value != self.original[key]:
                self.modified[key] = value
        else:
            self.added[key] = value

    def __delitem__(self, key):
        """Remove an item from the list.

        Deletes previous modifications.
        """
        if key in self.modified:
            del self.modified[key]
            self.deleted.add(key)
        elif key in self.added:
            del self.added[key]
        else:
            self.deleted.add(key)

    def get_changes(self, remote):
        """Compute all changes from a 'remote' dict.

        Yiels:
            Change object for each locally or remotely modified object.
        """
        seen = set()

        for k, v in self.modified.items():
            seen.add(k)
            yield Change(k, self.original[k], v, remote.get(k))

        for k in self.deleted.items():
            seen.add(k)
            yield Change(k, self.original[k], None, remote.get(k))

        for k, v in self.added.items():
            seen.add(k)
            yield Change(k, None, v, None)

        for k, v in self.original.items():
            if k not in seen and remote.get(k) != v:
                seen.add(k)
                # Remote deleted or changed
                yield Change(k, v, v, remote.get(k))

        for k, v in remote.items():
            if k not in seen:
                seen.add(k)
                # Remote added
                yield Change(k, None, None, v)

    def apply_change(self, k, action, new_value):
        """Apply a change.

        Args:
            k: the key of the item to change
            action: one of Change.ACTION_*, describes the action to perform
            new_value: object, the new value to use
        """
        if action == Change.ACTION_SKIP:
            return

        if action == Change.ACTION_ADD_REMOTE:
            self.connector.add_remote(k, new_value)
        elif action == Change.ACTION_UPDATE_REMOTE:
            self.connector.update_remote(k, new_value)
        elif action == Change.ACTION_REMOVE_REMOTE:
            self.connector.delete_remote(k)

        if new_value is None:
            del self.original[k]
        else:
            self.original[k] = new_value

        self.modified.pop(k, None)
        self.added.pop(k, None)
        self.removed.remove(k)

    def sync(self, change_handler, only_keys=()):
        """Synchronize the store with the remote.

        Args:
            change_handler: callable, should take a 'Change' object in and
                return a resolution mode.
            only_keys: tuple of keys to restrict change detection to.

        Returns:
            list of updated keys
        """
        remote = self.connector.fetch(only_keys)
        updated = []
        for change in self.get_changes(remote):
            if only_keys and change.key not in only_keys:
                continue
            if change.has_conflict():
                resolution_mode = change_handler(change)
            else:
                resolution_mode = None
            (action, new_value) = change.resolve(resolution_mode)
            self.apply_change(change.key, action, new_value)

            if action != Change.ACTION_SKIP:
                updated.append(change.key)

        return updated

    def last_sync(self):
        # TODO
        return None

    def save_to_disk(self, filename):
        # TODO
        pass
