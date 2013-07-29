# OMX package
# release 1

import tables;  # requires pytables >= 2.4

class File(tables.File):

    def createMatrix(self, name, atom=None, shape=None, title='', filters=None,
                     chunkshape=None, byteorder=None, createparents=False, obj=None,
                     tags=None):
        """Create OMX Matrix (CArray) at root level. User must pass in either
           an existing numpy matrix, or a shape and an atom type."""

        if tables.__version__.startswith('3'):
            matrix = self.createCArray(self.root, name, atom, shape, title, filters,
                                       chunkshape, byteorder, createparents, obj)
        else:
            # this version is tables 2.4-compatible:
            matrix = self.createCArray(self.root, name, atom, shape, title, filters,
                                       chunkshape, byteorder, createparents)
            if (obj != None):
                matrix[:] = obj

        matrix.attrs.tags = tags

        return matrix


    def shape(self):
        """Return the one and only shape of all matrices in this File"""
        if len(self) > 0:
            return self.iterNodes(self.root).next().shape
        else:
            return None


    def listMatrices(self):
        """Return list of Matrix names in this File"""
        return self.root._v_children


    def listAllTags(self):
        """Return combined list of all tags used for any Matrix in this File"""
        all_tags = set()
        for m in self.listNodes(self.root):
            if 'tags' in m.attrs and m.attrs.tags != None:
                all_tags.update(m.attrs.tags)
        return sorted(list(all_tags))



    # The following functions implement Python list/dictionary lookups. ----
    def __getitem__(self,key):
        """Return a matrix by name, or a list of matrices by tags"""

        if isinstance(key, str):
            return self.getNode(self.root, key)
        else:
            answer=[]

            # Loop on all matrices
            for m in self.listNodes(self.root):
                if 'tags' in m.attrs and m.attrs.tags != None:
                    # Test whether tags are a superset of the keys being requested
                    if set(m.attrs.tags).issuperset(key):
                        answer.append(m)

            return answer

    def __len__(self):
        return len(self.root._v_children)

    def __setitem__(self, key, dataset):
        # We need to determine atom and shape from the object that's been passed in.
        # This assumes 'dataset' is a numpy object.
        atom = tables.Atom.from_dtype(dataset.dtype)
        shape = dataset.shape

        return self.createMatrix(key, atom, shape, obj=dataset)

    def __delitem__(self, key):
        self.removeNode(self.root, key)

    def __iter__(self):
        """Iterate over the keys in this container"""
        return iter(self.root._v_children)

    def __contains__(self, item):
        return item in self.root._v_children


