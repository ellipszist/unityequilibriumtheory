"use client";

import React, { useState } from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical } from 'lucide-react';

export interface SortableItemType {
  id: string;
  content: React.ReactNode;
}

interface SortableItemProps {
  id: string;
  content: React.ReactNode;
}

export function SortableItem(props: SortableItemProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: props.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    zIndex: isDragging ? 10 : 1,
    position: 'relative' as const,
  };

  return (
    <div 
      ref={setNodeRef} 
      style={style} 
      className={`flex items-center gap-3 bg-white dark:bg-[#111] border border-black/10 dark:border-white/10 rounded-lg p-3 ${isDragging ? 'shadow-lg ring-2 ring-[#0d7a5f] opacity-80' : 'hover:border-black/20 dark:hover:border-white/20'} transition-colors`}
    >
      <div 
        {...attributes} 
        {...listeners}
        className="cursor-grab hover:bg-black/5 dark:hover:bg-white/5 p-1 rounded transition-colors text-black/40 dark:text-white/40"
      >
        <GripVertical size={18} />
      </div>
      <div className="flex-1">
        {props.content}
      </div>
    </div>
  );
}

interface SortableListProps {
  items: SortableItemType[];
  onReorder: (items: SortableItemType[]) => void;
}

export function SortableList({ items, onReorder }: SortableListProps) {
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;

    if (over && active.id !== over.id) {
      const oldIndex = items.findIndex((item) => item.id === active.id);
      const newIndex = items.findIndex((item) => item.id === over.id);
      
      onReorder(arrayMove(items, oldIndex, newIndex));
    }
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
    >
      <SortableContext
        items={items.map((i) => i.id)}
        strategy={verticalListSortingStrategy}
      >
        <div className="flex flex-col gap-2">
          {items.map((item) => (
            <SortableItem key={item.id} id={item.id} content={item.content} />
          ))}
        </div>
      </SortableContext>
    </DndContext>
  );
}
