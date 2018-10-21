import React from 'react'
import Downshift from 'downshift'
import api from 'tbot/api'

import './suggestinput.scss'

class SuggestChannelInput extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            channels: [],
        }
        this.fetch = this.fetch.bind(this)
        this.selected = this.selected.bind(this)
    }

    fetch(e) {
        if (!e.target.value) {
            this.setState({channels: []})
            return
        }
        api.get(`/api/twitch/channels`, {params:{suggest_name: e.target.value}}).then(r => {
            this.setState({
                channels: r.data, 
            })
        })
    }

    selected(s) {
        location.href = '/twitch/logviewer/'+s.name
    }

    render() {
        return (<Downshift 
                itemToString={item => (item ? item.name : '')}
                onChange={this.selected}
            >
            {({ 
                getLabelProps,
                getInputProps,
                getToggleButtonProps,
                getMenuProps,
                getItemProps,
                isOpen,
                clearSelection,
                selectedItem,
                inputValue,
                highlightedIndex,
            }) => (
                <div className="suggest-input">
                    <input {...getInputProps({
                        name: 'channel',
                        placeholder: 'Channel search',
                        onChange: this.fetch,
                        className: 'form-control',
                    })} />
                    {isOpen && (this.state.channels.length>0) ? (
                        <div className="suggest-container">{
                            this.state.channels.map((item, index) => (
                                <div
                                    className="suggest-item"
                                    {...getItemProps({ key: index, index, item })}
                                    style={{
                                        backgroundColor: highlightedIndex === index ? '#505258' : '#43464F',
                                        fontWeight: selectedItem === item ? 'bold' : 'normal',
                                    }}
                                >
                                    {item.name}
                                </div>
                            ))
                        }</div>
                    ) : null}
                </div>
            )}
        </Downshift>)
    }
}

export default SuggestChannelInput