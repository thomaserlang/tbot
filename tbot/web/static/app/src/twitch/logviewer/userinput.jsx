import React from 'react'
import Downshift from 'downshift'
import api from 'tbot/twitch/api'

import './suggestinput.scss'

class UserInput extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            users: [],
            value: this.props.defaultValue,
        }
        this.fetchUsers = this.fetchUsers.bind(this)
        this.stateChange = this.stateChange.bind(this)
    }

    fetchUsers(e) {
        if (!e.target.value) {
            this.setState({users: []})
            return
        }
        api.get(`/api/twitch/channels/${this.props.channel_id}/users`, {params:{suggest_name: e.target.value}}).then(r => {
            this.setState({
                users: r.data, 
            })
        })
    }

    stateChange(e) {
        console.log(e)
        switch (e.type) {
            case Downshift.stateChangeTypes.clickItem:
            case Downshift.stateChangeTypes.changeInput:
                this.setState({value: (e.inputValue ? e.inputValue: e.selectedItem.name)})
            break
            case Downshift.stateChangeTypes.keyDownArrowUp:
            case Downshift.stateChangeTypes.keyDownArrowDown:
                this.setState({value: (this.state.users[e.highlightedIndex].name)})
            break
        }     
    }
      
    render() {
        return (<Downshift 
                inputValue={this.state.value}
                onStateChange={this.stateChange}
                itemToString={item => (item ? item.name : '')}
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
                        name: 'user',
                        placeholder: 'User',
                        onChange: this.fetchUsers,
                        className: 'form-control',
                    })} />
                    {isOpen && (this.state.users.length>0) ? (
                        <div className="suggest-container">{
                            this.state.users.map((item, index) => (
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

export default UserInput