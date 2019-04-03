"""A simple yet powerful abstract tree data structure."""

from abc import ABCMeta, abstractmethod, abstractproperty
from inspect import isclass

from six import reraise, with_metaclass
import zetup

import moretools

__all__ = ('SimpleTree', )


class SimpleTreeMeta(zetup.meta, ABCMeta):
    """
    Metaclass for abstract :class:`moretools.SimpleTree`.

    Creates the context stacks for classes derived from :class:`SimpleTree`

    The context manager of tree instances puts them on the associated context
    stack as implicit parents for tree instances created in the context code
    block, so that they can be automatically registered as sub-trees

    See :class:`moretools.SimpleTree` for more details
    """

    context_stack = None

    def __new__(mcs, clsname, bases, clsattrs):
        if mcs.context_stack is None:

            class meta(mcs):
                context_stack = []

        else:
            meta = mcs
        return ABCMeta.__new__(meta, clsname, bases, clsattrs)


class SimpleTree(with_metaclass(SimpleTreeMeta, zetup.object)):
    r"""
    The simple yet powerful tree creation and processing factory.

    This class is abstract and must be derived with an actual implementation
    of the hierarchical linkings in the tree, handled by abstract
    :prop:`.parent` and :meth:`.sub`

    It's important that the ``@parent.setter`` takes care of linking a
    sub-tree to the parent, and the :meth:`.sub` implementation for accessing
    sub-trees should support custom ``*filters`` and ``**kwfilters``. More
    detailed information is given in those abstract members' doc strings. A
    sample implementation could look like:

    >>> from moretools import SimpleTree

    >>> class ActualTree(SimpleTree):
    ...
    ...     def __init__(self, node_data):
    ...         super(ActualTree, self).__init__()
    ...         self._children = []
    ...         self.data = node_data
    ...
    ...     @property
    ...     def parent(self):
    ...         return self._parent
    ...
    ...     @parent.setter
    ...     def parent(self, tree):
    ...         if tree is not None:
    ...             tree._children.append(self)
    ...
    ...     def sub(self, *filters, **kwfilters):
    ...         for item in self._children:
    ...             if all (f(item) for f in filters):
    ...                 yield item
    ...
    ...     def __repr__(self, indent=0):
    ...         text = ' ' * indent + str(self.data).join('[]')
    ...         if self._children:
    ...             text = '\n'.join((text, '\n'.join(
    ...                 item.__repr__(indent + 4) for item in self._children)))
    ...         return text

    Now tree structures can simply be created using context blocks:

    >>> with ActualTree("root") as tree:
    ...     with ActualTree("some-sub"):
    ...         ActualTree("sub-sub")
    ...     ActualTree("other-sub")
    [...
    >>> tree
    [root]
        [some-sub]
            [sub-sub]
        [other-sub]

    And :meth:`.sub` can be used for accessing sub-trees:

    >>> tuple(tree.sub(lambda item: item.data.startswith('some')))
    ([some-sub]
        [sub-sub],)
    """

    # used by zetup.meta's class __repr__ instead of __module__
    __package__ = moretools

    def __init__(self, parent=None):
        if parent is None:
            meta = type(type(self))
            if meta.context_stack:
                parent = meta.context_stack[-1]
        self.parent = parent

        cls = type(self)
        if isclass(cls.sub):
            self.sub = cls.sub(owner=self)

    def root(self):
        """
        Get the root tree of this sub-tree.

        Returns this tree itself if not a sub-tree
        """
        tree = self
        while tree.parent is not None:
            tree = tree.parent
        return tree

    @abstractproperty
    def parent(self):
        """
        Get and set parent tree of this sub-tree.

        This property is abstract and must be overridden with an actual
        implementation

        Should return ``None`` if not a sub-tree

        The ``@parent.setter`` method must also take care of registering this
        tree as a sub-tree to the parent
        """
        pass

    @abstractmethod
    def sub(self, *filters, **kwfilters):
        """
        Get the direct sub-trees of this tree.

        Supporting filter options

        This method is abstract and must be overridden with an actual
        implementation, which can alternatively be a class. In the latter
        case, it gets automatically instantiated without arguments and
        assigned to ``self.sub`` in :meth:`.__init__`
        """
        pass

    def __enter__(self):
        meta = type(type(self))
        meta.context_stack.append(self)
        return self

    def __exit__(self, *exc_info):
        meta = type(type(self))
        stack = meta.context_stack
        assert stack and stack[-1] is self, (
            "Corrupted .context_stack of {!r}".format(meta))

        meta.context_stack.pop(-1)
        if exc_info[0] is not None:
            reraise(*exc_info)
