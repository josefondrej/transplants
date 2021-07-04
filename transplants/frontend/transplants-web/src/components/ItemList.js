import React from 'react';
import chroma from 'chroma-js';


import Select from 'react-select';

const dot = (color = '#ccc') => ({
    alignItems: 'center',
    display: 'flex',

    ':before': {
        backgroundColor: color,
        borderRadius: 10,
        content: '" "',
        display: 'block',
        marginRight: 8,
        height: 10,
        width: 10,
    },
});
const colourStyles = {
    control: (styles) => ({...styles, backgroundColor: '#fff', fontFamily: 'Arial', zoom: '90%'}),
    option: (styles, {data, isDisabled, isFocused, isSelected}) => {
        const color = chroma(data.color);
        return {
            ...styles,
            zoom: '90%',
            fontFamily: 'Arial',
            backgroundColor: isDisabled
                ? null
                : isSelected
                    ? data.color
                    : isFocused
                        ? color.alpha(0.1).css()
                        : null,
            color: isDisabled
                ? '#ccc'
                : isSelected
                    ? chroma.contrast(color, 'white') > 2
                        ? 'white'
                        : 'black'
                    : data.color,
            cursor: isDisabled ? 'not-allowed' : 'default',

            ':active': {
                ...styles[':active'],
                backgroundColor:
                    !isDisabled && (isSelected ? data.color : color.alpha(0.3).css()),
            },
        };
    },
    singleValue: (styles, {data}) => ({
        ...styles,
        ...dot(data.color)
    }),
    multiValue: (styles, {data}) => {
        const color = chroma(data.color);
        return {
            ...styles,
            backgroundColor: color.alpha(0.1).css(),
        };
    },
    multiValueLabel: (styles, {data}) => ({
        ...styles,
        color: data.color,
    }),
    multiValueRemove: (styles, {data}) => ({
        ...styles,
        color: data.color,
        ':hover': {
            backgroundColor: data.color,
            color: 'white',
        },
    }),
};

export default function ItemList(props) {
    return (<Select
        closeMenuOnSelect={false}
        defaultValue={[]}
        isMulti={props.isMulti}
        isDisabled={!props.editable}
        options={props.options}
        styles={colourStyles}
    />)
}