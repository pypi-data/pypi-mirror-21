#pragma once
// #include "lue/c_api/collection.h"
#include "lue/hdf5/group.h"
#include <cassert>
#include <map>
#include <memory>
#include <stdexcept>
#include <vector>


namespace lue {

// bool               collection_exists   (hdf5::Identifier const& location,
//                                         std::string const& name);


/*!
    The collection is modeled using an HDF5 group.
*/
template<
    typename T>
class Collection:
    public hdf5::Group
{

public:

    bool           empty               () const;

    size_t         size                () const;

    std::vector<std::string>
                   names               () const;

    bool           contains            (std::string const& name) const;

    T&             operator[]          (std::string const& name) const;

                   Collection          (Group&& group);

                   Collection          (Collection&& other)=default;

                   ~Collection         ()=default;

    T&             add                 (std::string const& name,
                                        T&& item);

protected:

                   Collection          (hdf5::Identifier const& location,
                                        std::string const& name);

                   Collection          (hdf5::Identifier&& id);

                   Collection          (Collection const& other)=delete;

    Collection&    operator=           (Collection const& other)=delete;

    Collection&    operator=           (Collection&& other)=default;

private:

    // std::string const& _name;

    std::vector<std::string>
                   item_names          () const;

    std::map<std::string, std::unique_ptr<T>> _items;

};


// std::vector<std::string>
//                    item_names          (hdf5::Identifier const& location);

template<
    typename T>
Collection<T>      create_collection   (hdf5::Identifier const& location,
                                        std::string const& name);


/*!
    @brief      Constructor
    @param      location Identifier of file or group of group to open
    @exception  std::runtime_error In case the group cannot be opened
*/
template<
    typename T>
inline Collection<T>::Collection(
    hdf5::Identifier const& location,
    std::string const& name)

    : hdf5::Group(location, name.c_str()),
      // _name(name),
      _items{}

{
    if(!id().is_valid()) {
        throw std::runtime_error("Collection " + name + " cannot be opened");
    }

    // Open items, if available.
    for(auto const& name: item_names()) {
        _items.insert(std::make_pair(name, std::make_unique<T>(id(), name)));
    }
}


template<
    typename T>
inline Collection<T>::Collection(
    hdf5::Identifier&& id)

    : hdf5::Group(std::forward<hdf5::Identifier>(id)),
      // _name(name),
      _items{}

{
    // Open items, if available.
    for(auto const& name: item_names()) {
        _items.insert(std::make_pair(name, std::make_unique<T>(this->id(),
            name)));
    }
}


template<
    typename T>
inline Collection<T>::Collection(
    hdf5::Group&& group)

    : hdf5::Group(std::forward<hdf5::Group>(group)),
      _items{}

{
    // Open items, if available.
    for(auto const& name: item_names()) {
        _items.insert(std::make_pair(name, std::make_unique<T>(this->id(),
            name)));
    }
}


template<
    typename T>
inline bool Collection<T>::empty() const
{
    return _items.empty();
}


template<
    typename T>
inline size_t Collection<T>::size() const
{
    return _items.size();
}


/*!
    @brief      Return names of items
*/
template<
    typename T>
inline std::vector<std::string> Collection<T>::names() const
{
    std::vector<std::string> names;
    names.reserve(_items.size());

    for(auto const& pair: _items) {
        names.emplace_back(pair.first);
    }

    return names;
}


/*!
    @brief      Add an item to the collection
    @param      name Name of item to add
    @param      item Item to add
    @return     A reference to the added item
*/
template<
    typename T>
inline T& Collection<T>::add(
    std::string const& name,
    T&& item)
{
    auto pair = _items.insert(std::make_pair(name, std::make_unique<T>(
        std::forward<T>(item))));
    assert(pair.second);

    return *(*pair.first).second;
}


/*!
    @brief      Return whether or not the collection contains an item with
                the name passed in
    @param      name Name of item
*/
template<
    typename T>
inline bool Collection<T>::contains(
    std::string const& name) const
{
    return _items.find(name) != _items.end();
}


/*!
    @brief      Return item
    @param      name Name of item
    @exception  std::runtime_error In case the item does not exist
*/
template<
    typename T>
inline T& Collection<T>::operator[](
    std::string const& name) const
{
    auto iterator = _items.find(name);

    if(iterator == _items.end()) {
        throw std::runtime_error("Item " + name + " does not exist");
    }

    return *(*iterator).second;
}


template<
    typename T>
inline std::vector<std::string> Collection<T>::item_names() const
{
    return group_names();
}


template<
    typename T>
Collection<T> create_collection(
    hdf5::Identifier const& location,
    std::string const& name)
{
    return hdf5::create_group(location, name);
}

} // namespace lue
