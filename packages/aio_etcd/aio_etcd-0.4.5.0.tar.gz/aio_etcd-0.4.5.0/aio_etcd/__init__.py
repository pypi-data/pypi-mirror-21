import logging
from etcd import *
from .client import Client
from .lock import Lock

__VERSION__ = (0,4,5,0)

_log = logging.getLogger(__name__)

class StopWatching(BaseException):
    pass

_EtcdResult = EtcdResult
class EtcdResult(_EtcdResult):
    def parse_headers(self, response):
        headers = response.headers
        self.etcd_index = int(headers.get('x-etcd-index', 1))
        self.raft_index = int(headers.get('x-raft-index', 1))

    def get_subtree(self, leaves_only=False):
        """
        Get all the subtree resulting from a recursive=true call to etcd.

        Args:
            leaves_only (bool): if true, only value nodes are returned


        """
        if not self._children:
            #if the current result is a leaf, return itself
            yield self
            return
        else:
            # node is not a leaf
            if not leaves_only:
                yield self
            for n in self._children:
                node = EtcdResult(None, n)
                for child in node.get_subtree(leaves_only=leaves_only):
                    yield child
        return

    @property
    def leaves(self):
        return self.get_subtree(leaves_only=True)

    @property
    def children(self):
        """ Deprecated, use EtcdResult.leaves instead """
        return self.leaves

    def __eq__(self, other):
        if not (type(self) is type(other)):
            return False
        for k in self._node_props.keys():
            try:
                a = getattr(self, k)
                b = getattr(other, k)
                if a != b:
                    return False
            except:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class EtcdException(Exception):

    """
    Generic Etcd Exception.
    """
    def __init__(self, message=None, payload=None):
        super(EtcdException, self).__init__(message)
        self.payload = payload


class EtcdValueError(EtcdException, ValueError):
    """
    Base class for Etcd value-related errors.
    """
    pass


class EtcdCompareFailed(EtcdValueError):
    """
    Compare-and-swap failure
    """
    pass


class EtcdClusterIdChanged(EtcdException):
    """
    The etcd cluster ID changed.  This may indicate the cluster was replaced
    with a backup.  Raised to prevent waiting on an etcd_index that was only
    valid on the old cluster.
    """
    pass


class EtcdKeyError(EtcdException):
    """
    Etcd Generic KeyError Exception
    """
    pass


class EtcdKeyNotFound(EtcdKeyError):
    """
    Etcd key not found exception (100)
    """
    pass


class EtcdNotFile(EtcdKeyError):
    """
    Etcd not a file exception (102)
    """
    pass


class EtcdNotDir(EtcdKeyError):
    """
    Etcd not a directory exception (104)
    """
    pass


class EtcdAlreadyExist(EtcdKeyError):
    """
    Etcd already exist exception (105)
    """
    pass


class EtcdEventIndexCleared(EtcdException):
    """
    Etcd event index is outdated and cleared exception (401)
    """
    pass


class EtcdConnectionFailed(EtcdException):
    """
    Connection to etcd failed.
    """
    def __init__(self, message=None, payload=None, cause=None):
        super(EtcdConnectionFailed, self).__init__(message=message,
                                                   payload=payload)
        self.cause = cause


class EtcdInsufficientPermissions(EtcdException):
    """
    Request failed because of insufficient permissions.
    """
    pass


class EtcdWatchTimedOut(EtcdConnectionFailed):
    """
    A watch timed out without returning a result.
    """
    pass


class EtcdWatcherCleared(EtcdException):
    """
    Watcher is cleared due to etcd recovery.
    """
    pass


class EtcdLeaderElectionInProgress(EtcdException):
    """
    Request failed due to in-progress leader election.
    """
    pass


class EtcdRootReadOnly(EtcdKeyError):
    """
    Operation is not valid on the root, which is read only.
    """
    pass


class EtcdDirNotEmpty(EtcdValueError):
    """
    Directory not empty.
    """
    pass


class EtcdLockExpired(EtcdException):
    """
    Our lock apparently expired while we were trying to acquire it.
    """
    pass


class EtcdError(object):
    # See https://github.com/coreos/etcd/blob/master/Documentation/v2/errorcode.md
    error_exceptions = {
        100: EtcdKeyNotFound,
        101: EtcdCompareFailed,
        102: EtcdNotFile,
        # 103: Non-public: no more peers.
        104: EtcdNotDir,
        105: EtcdAlreadyExist,
        # 106: Non-public: key is preserved.
        107: EtcdRootReadOnly,
        108: EtcdDirNotEmpty,
        # 109: Non-public: existing peer addr.
        110: EtcdInsufficientPermissions,

        200: EtcdValueError,  # Not part of v2
        201: EtcdValueError,
        202: EtcdValueError,
        203: EtcdValueError,
        204: EtcdValueError,
        205: EtcdValueError,
        206: EtcdValueError,
        207: EtcdValueError,
        208: EtcdValueError,
        209: EtcdValueError,
        210: EtcdValueError,

        # 300: Non-public: Raft internal error.
        301: EtcdLeaderElectionInProgress,

        400: EtcdWatcherCleared,
        401: EtcdEventIndexCleared,
    }

    @classmethod
    def handle(cls, payload):
        """
        Decodes the error and throws the appropriate error message

        :param payload: The decoded JSON error payload as a dict.
        """
        error_code = payload.get("errorCode")
        message = payload.get("message")
        cause = payload.get("cause")
        msg = '{} : {}'.format(message, cause)
        status = payload.get("status")
        # Some general status handling, as
        # not all endpoints return coherent error messages
        if status == 404:
            error_code = 100
        elif status == 401:
            error_code = 110
        exc = cls.error_exceptions.get(error_code, EtcdException)
        if issubclass(exc, EtcdException):
            raise exc(msg, payload)
        else:
            raise exc(msg)


# Attempt to enable urllib3's SNI support, if possible
# Blatantly copied from requests.
try:
    from urllib3.contrib import pyopenssl
    pyopenssl.inject_into_urllib3()
except ImportError:
    pass
