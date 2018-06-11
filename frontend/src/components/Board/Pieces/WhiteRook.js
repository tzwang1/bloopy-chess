import React, { Component } from 'react';
import Draggable from 'react-draggable';

class WhiteRook extends Component {
    constructor(props) {
        super(props)
        this.state = {
            gridPosition: {
                x: 0,
                y: 0
            }
        }
        this.tileSize = props.tileSize;
        this.matrixPos = this.props.pos;
    }
    
    onStart = () => {
        // console.log(this.state.pos);
        let activeDrags = this.state.activeDrags
        this.setState({activeDrags: ++activeDrags});
    }

    onStop = (event, drag) => {
        let activeDrags = this.state.activeDrags
        this.setState({activeDrags: --activeDrags});
    }

    adjustPos = (pos) => {
        let new_pos;
        if(Math.abs(pos % this.tileSize) > Math.floor(this.tileSize/2)) {
            if(pos > 0) {
                new_pos = pos + (this.tileSize - (pos % this.tileSize));
            } else {
                new_pos = pos - (this.tileSize + (pos % this.tileSize));
            }
        } else {
            new_pos = pos - (pos % this.tileSize);
        }
        return new_pos
    }

    onControlledDrag = (e, position) => {
        let {x, y} = position;
        // console.log("position", position);
        let oldGridX = this.state.gridPosition.x;
        let oldGridY = this.state.gridPosition.y;

        x = this.adjustPos(x);
        y = this.adjustPos(y);

        this.setState({gridPosition: {x, y}});
    
        let newRow = ((y - oldGridY) / this.tileSize) + this.matrixPos[0];
        let newCol = ((x - oldGridX) / this.tileSize) + this.matrixPos[1];
        this.matrixPos = [newRow, newCol];
    }
    
    onControlledDragStop = (e, position) => {
        this.onControlledDrag(e, position);
        this.onStop();
    }
    
    render() {
        // console.log("Rendering black bishop");
        // console.log("Controlled Position", this.state.gridPosition);
        // console.log("Position", this.matrixPos);
        const gridPosition = this.state.gridPosition;
        const dragHandlers = {onStart: this.onStart, onStop: this.onControlledDragStop};
        return(
            <Draggable disabled={false} position={gridPosition} bounds="parent" {...dragHandlers}>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45" height="100%">
                    <g
                        fill="#fff"
                        fillRule="evenodd"
                        stroke="#000"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round">
                        <path
                        d="M9 39h27v-3H9v3zM12 36v-4h21v4H12zM11 14V9h4v2h5V9h5v2h5V9h4v5"
                        strokeLinecap="butt"
                        />
                        <path d="M34 14l-3 3H14l-3-3" />
                        <path d="M31 17v12.5H14V17" strokeLinecap="butt" strokeLinejoin="miter" />
                        <path d="M31 29.5l1.5 2.5h-20l1.5-2.5" />
                        <path d="M11 14h23" fill="none" strokeLinejoin="miter" />
                    </g>
                </svg>
            </Draggable>
        );
    }
}

export default WhiteRook;