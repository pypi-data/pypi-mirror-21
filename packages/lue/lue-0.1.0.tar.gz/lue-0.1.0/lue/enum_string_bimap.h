#pragma once
#include <boost/bimap.hpp>
#include <cassert>
#include <string>


namespace lue {
namespace detail {

template<
    typename T>
class EnumStringBimap
{

public:

    using Map = boost::bimap<T, std::string>;
    using value_type = typename Map::value_type;

                   EnumStringBimap     ()=default;

                   EnumStringBimap     (std::initializer_list<value_type>
                                            const& values);

                   EnumStringBimap     (EnumStringBimap const&)=default;

                   EnumStringBimap     (EnumStringBimap&&)=default;

                   ~EnumStringBimap    ()=default;

    EnumStringBimap&
                   operator=           (EnumStringBimap const&)=default;

    EnumStringBimap&
                   operator=           (EnumStringBimap&&)=default;

    bool           contains            (std::string const& string) const;

    T              as_value            (std::string const& string) const;

    std::string    as_string           (T const value) const;

private:

    Map            _map;

};


template<
    typename T>
EnumStringBimap<T>::EnumStringBimap(
    std::initializer_list<value_type> const& values)

    : _map(values.begin(), values.end())

{
}


template<
    typename T>
bool EnumStringBimap<T>::contains(
    std::string const& string) const
{
    return _map.right.find(string) != _map.right.end();
}


template<
    typename T>
T EnumStringBimap<T>::as_value(
    std::string const& string) const
{
    assert(contains(string));

    return _map.right.at(string);
}


template<
    typename T>
std::string EnumStringBimap<T>::as_string(
    T const value) const
{
    assert(_map.left.find(value) != _map.left.end());

    return _map.left.at(value);
}

}  // namespace detail
}  // namespace lue
