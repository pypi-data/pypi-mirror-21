#pragma once
#include "lue/hdf5/identifier.h"
#include "lue/hdf5/dataspace.h"
#include "lue/hdf5/datatype.h"
#include "lue/hdf5/datatype_traits.h"
#include <cassert>


namespace lue {
namespace hdf5 {

/*!
    @brief      This class represents an attribute attached to an object
*/
class Attribute
{

public:

//                    Attribute           (Identifier const& location,
//                                         std::string const& name,
//                                         Datatype const& datatype,
//                                         Dataspace const& dataspace);

                   Attribute           (Identifier&& id);

                   Attribute           (Identifier const& location,
                                        std::string const& name);

                   Attribute           (Attribute const& other)=delete;

                   Attribute           (Attribute&& other)=default;

                   ~Attribute          ()=default;

    Attribute&     operator=           (Attribute const& other)=delete;

    Attribute&     operator=           (Attribute&& other)=default;

    Identifier const& id               () const;

    Datatype const& datatype           () const;

    template<
        typename T>
    void           write               (T const& value);

    template<
        typename T>
    T              read                () const;

private:

    //! Identifier of object owning the attribute
    Identifier     _id;

    //! Datatype of attribute
    Datatype       _datatype;

};


template<>
inline std::string Attribute::read<std::string>() const
{
    static_assert(std::is_same<std::string::value_type, char>::value,
        "expect std::string::value_type to be char");

    assert(_datatype.encoding() == ::H5T_CSET_UTF8);

    auto const nr_bytes = _datatype.size();

    std::string result(nr_bytes, 'x');

    auto status = ::H5Aread(_id, _datatype.id(),
#if __cplusplus > 201402L
        result.data()
#else
        const_cast<std::string::value_type*>(result.data())
#endif
    );
    assert(result.size() == nr_bytes);

    if(status < 0) {
        throw std::runtime_error("Cannot read attribute");
    }

    return result;
}


template<>
inline std::vector<unsigned char>
    Attribute::read<std::vector<unsigned char>>() const
{
    auto const nr_bytes = _datatype.size();

    std::vector<unsigned char> result(nr_bytes);

    auto status = ::H5Aread(_id, _datatype.id(), result.data());
    assert(result.size() == nr_bytes);

    if(status < 0) {
        throw std::runtime_error("Cannot read attribute");
    }

    return result;
}


template<
    typename T>
inline T Attribute::read() const
{
    T value;
    auto status = ::H5Aread(_id, _datatype.id(), &value);

    if(status < 0) {
        throw std::runtime_error("Cannot read attribute");
    }

    return value;
}


template<>
inline void Attribute::write<std::string>(
    std::string const& value)
{
    auto status = ::H5Awrite(_id, _datatype.id(), value.c_str());

    if(status < 0) {
        throw std::runtime_error("Cannot write attribute");
    }
}


template<>
inline void Attribute::write<std::vector<unsigned char>>(
    std::vector<unsigned char> const& value)
{
    auto status = ::H5Awrite(_id, _datatype.id(), value.data());

    if(status < 0) {
        throw std::runtime_error("Cannot write attribute");
    }
}


template<
    typename T>
inline void Attribute::write(
    T const& value)
{
    auto status = ::H5Awrite(_id, _datatype.id(), &value);

    if(status < 0) {
        throw std::runtime_error("Cannot write attribute");
    }
}


// Attribute          create_attribute    (Identifier const& location,
//                                         std::string const& name,
//                                         std::string const& value);
// 
// Attribute          create_attribute    (Identifier const& location,
//                                         std::string const& name,
//                                         std::vector<unsigned char> const& value);


// Attribute          create_attribute    (Identifier const& location,
//                                         std::string const& name,
//                                         size_t const nr_bytes);

Attribute          create_attribute    (Identifier const& location,
                                        std::string const& name,
                                        Datatype const& datatype,
                                        Dataspace const& dataspace);


template<
    typename T>
Attribute          create_attribute    (Identifier const& location,
                                        std::string const& name,
                                        T const& value);


template<>
inline Attribute create_attribute(
    Identifier const& location,
    std::string const& name,
    std::string const& value)
{
    auto attribute = create_attribute(location, name,
        create_datatype(value.size()), Dataspace(::H5S_SCALAR));
    attribute.write(value);

    return attribute;
}


template<>
inline Attribute create_attribute<std::vector<unsigned char>>(
    Identifier const& location,
    std::string const& name,
    std::vector<unsigned char> const& value)
{
    auto attribute = create_attribute(location, name,
        create_datatype(H5T_NATIVE_UCHAR, value.size()),
        Dataspace(::H5S_SCALAR));
    attribute.write(value);

    return attribute;
}


template<
    typename T>
inline Attribute create_attribute(
    Identifier const& location,
    std::string const& name,
    T const& value)
{
    auto attribute = create_attribute(location, name,
        Datatype(NativeDatatypeTraits<T>::type_id()),
        Dataspace(::H5S_SCALAR));
    attribute.write(value);

    return attribute;
}

} // namespace hdf5
} // namespace lue
