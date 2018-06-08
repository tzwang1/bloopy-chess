import React, { Component } from 'react';
import Draggable from 'react-draggable';

class BlackQueen extends Component {
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
        console.log("position", position);
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
        console.log("Rendering black bishop");
        console.log("Controlled Position", this.state.gridPosition);
        console.log("Position", this.matrixPos);
        const gridPosition = this.state.gridPosition;
        const dragHandlers = {onStart: this.onStart, onStop: this.onControlledDragStop};
        return(
            <Draggable disabled={false} position={gridPosition} bounds="parent" {...dragHandlers}>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45" height="100%">
                    <g
                        fill={0}
                        fillRule="evenodd"
                        stroke="#000"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round">
                        <g fill="#000" stroke="none">
                        <circle cx={6} cy={12} r={2.75} />
                        <circle cx={14} cy={9} r={2.75} />
                        <circle cx={22.5} cy={8} r={2.75} />
                        <circle cx={31} cy={9} r={2.75} />
                        <circle cx={39} cy={12} r={2.75} />
                        </g>
                        <path
                        d="M9 26c8.5-1.5 21-1.5 27 0l2.5-12.5L31 25l-.3-14.1-5.2 13.6-3-14.5-3 14.5-5.2-13.6L14 25 6.5 13.5 9 26z"
                        strokeLinecap="butt"
                        />
                        <path
                        d="M9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 16.5 1 23 0 0 0 1.5-1 0-2.5 0 0 .5-1.5-1-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z"
                        strokeLinecap="butt"
                        />
                        <path d="M11 38.5a35 35 1 0 0 23 0" fill="none" strokeLinecap="butt" />
                        <path
                        d="M11 29a35 35 1 0 1 23 0M12.5 31.5h20M11.5 34.5a35 35 1 0 0 22 0M10.5 37.5a35 35 1 0 0 24 0"
                        fill="none"
                        stroke="#fff"
                        />
                    </g>
                </svg>
            </Draggable>
        );
    }
}

export default BlackQueen;