#!/usr/bin/env python
# coding: utf-8

import ACC_Main
def originalStylize(df):
    return df.style.set_caption("Review the Member's form, and pick a work flow:").highlight_null(null_color='pink').set_table_styles([{
        'selector': 'caption',
        'props': [
            ('color', 'black'),
            ('font-size', '30px'),
            ('background-color', 'lightyellow')
        ]
    }])


def templateStylize(df):
    
    return df.fillna('').style.set_caption("Double check your work and convert this form to .CSV").set_table_styles([{
        'selector': 'caption',
        'props': [
            ('color', 'black'),
            ('font-size', '30px'),
            ('background-color', 'lightyellow')
        ]
    }])
    #df.highlight_null(null_color='pink') - this highlights the cell with NaN exists

def addressCompleted_Stylize(df):
    return df.style.set_caption("Address's Completed:").highlight_null(null_color='pink').set_table_styles([{
        'selector': 'caption',
        'props': [
            ('color', 'black'),
            ('font-size', '30px'),
            ('background-color', 'lightgreen'),
            ('width', '750px')
        ]
    }])

# display large dataframes in an html iframe
def addressChecker_Stylize(df):
    return df.style.set_caption("Choose the Best Match:").highlight_null(null_color='pink').set_table_styles([{
        'selector': 'caption',
        'props': [
            ('color', 'black'),
            ('font-size', '30px'),
            ('background-color', 'lightblue'),
            ('width', '750px')
        ]
    }])

def addressModify_Stylize(df):
    return df.style.hide_index().set_caption("Manually Update Submission:").set_table_styles([{
        'selector': 'caption',
        'props': [
            ('color', 'black'),
            ('font-size', '30px'),
            ('background-color', 'plum'),
            ('width', '750px')
        ]
    }])
