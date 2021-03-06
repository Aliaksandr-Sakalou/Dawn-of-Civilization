/*=============================================================================
    Copyright (c) 2003 Joel de Guzman

    Use, modification and distribution is subject to the Boost Software
    License, Version 1.0. (See accompanying file LICENSE_1_0.txt or copy at
    http://www.boost.org/LICENSE_1_0.txt)
==============================================================================*/
#if !defined(FUSION_SEQUENCE_AS_FUSION_ITERATOR_HPP)
#define FUSION_SEQUENCE_AS_FUSION_ITERATOR_HPP

#include <boost/spirit/fusion/iterator/is_iterator.hpp>
#include <boost/spirit/fusion/iterator/type_sequence_iterator.hpp>
#include <boost/mpl/if.hpp>
#include <boost/mpl/bool.hpp>

namespace boost { namespace fusion
{
    //  Test T. If it is a fusion iterator, return a reference to it.
    //  else, assume it is an mpl iterator.

    template <typename T>
    struct as_fusion_iterator
    {
        typedef typename
            mpl::if_<
                fusion::is_iterator<T>
              , T
              , type_sequence_iterator<T>
            >::type
        type;

        static T const&
        convert(T const& x, mpl::true_)
        {
            return x;
        }

        static type_sequence_iterator<T>
        convert(T const& x, mpl::false_)
        {
            return type_sequence_iterator<T>();
        }

        static typename
            mpl::if_<
                fusion::is_iterator<T>
              , T const&
              , type_sequence_iterator<T>
            >::type
        convert(T const& x)
        {
            return convert(x, fusion::is_iterator<T>());
        }
    };
}}

#endif
